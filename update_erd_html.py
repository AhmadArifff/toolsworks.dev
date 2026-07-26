import re

def update_erd(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace renderClusterSVG with renderClusterCanvasHtml and mount Cluster Canvas methods
    old_render_svg_pattern = r'renderClusterSVG\(cluster\)\s*\{[\s\S]*?\n    \}'
    
    new_methods = '''initClusterCanvasState(cluster) {
      if (cluster.canvasState) return;
      const tables = [...new Set(cluster.members.map(m => m.table))];
      const colForTable = {};
      cluster.members.forEach(m => { if (!colForTable[m.table]) colForTable[m.table] = m.col; });
      const nodes = {};
      const numCols = Math.min(3, Math.ceil(Math.sqrt(tables.length)));
      tables.forEach((t, i) => {
        const col = i % numCols;
        const row = Math.floor(i / numCols);
        nodes[t] = { table: t, col: colForTable[t], x: 40 + col * 250, y: 30 + row * 140, w: 200, h: 70 };
      });
      cluster.canvasState = {
        nodes,
        zoom: 0.85,
        panX: 30,
        panY: 30
      };
    }

    renderClusterCanvasHtml(cluster, idx) {
      this.initClusterCanvasState(cluster);
      const zoomPct = Math.round(cluster.canvasState.zoom * 100);
      return `
        <div class="relative w-full h-[320px] bg-[#0A0E14] border border-white/10 rounded-xl overflow-hidden select-none mb-3 cluster-viewport cursor-grab" data-cluster="${idx}">
          <div class="absolute inset-0 pointer-events-none" style="background-image: radial-gradient(#1C2530 1.4px, transparent 1.4px); background-size: 24px 24px;"></div>
          <div class="absolute top-2.5 right-2.5 z-20 flex items-center gap-1 bg-[#0D1219]/90 border border-white/10 rounded-lg p-1 font-mono">
            <button type="button" class="cluster-btn-zoom-out w-7 h-7 rounded hover:bg-white/10 text-slate-300 font-bold flex items-center justify-center text-xs" data-cluster="${idx}">-</button>
            <span class="cluster-zoom-label w-11 text-center font-mono text-[11px] text-slate-400 select-none" data-cluster="${idx}">${zoomPct}%</span>
            <button type="button" class="cluster-btn-zoom-in w-7 h-7 rounded hover:bg-white/10 text-slate-300 font-bold flex items-center justify-center text-xs" data-cluster="${idx}">+</button>
            <button type="button" class="cluster-btn-fit px-2 h-7 rounded hover:bg-white/10 text-slate-300 font-mono text-[11px]" data-cluster="${idx}">Fit</button>
          </div>
          <div class="absolute bottom-2 left-2.5 z-10 text-[10px] text-slate-500 font-mono pointer-events-none">
            ✦ Drag tabel untuk menggeser · Scroll untuk Zoom · Drag latar untuk Pan
          </div>
          <div class="cluster-world absolute top-0 left-0 origin-top-left" data-cluster="${idx}">
            <svg class="cluster-svg absolute top-0 left-0 overflow-visible pointer-events-none" data-cluster="${idx}"></svg>
            <div class="cluster-cards-layer absolute top-0 left-0" data-cluster="${idx}"></div>
          </div>
        </div>`;
    }

    mountClusterCanvas(idx) {
      const cluster = this.valueClusters && this.valueClusters[idx];
      if (!cluster) return;
      this.initClusterCanvasState(cluster);
      const cardEl = this.$.summaryBody.querySelector(`[data-cluster-card="${idx}"]`);
      if (!cardEl) return;

      const viewport = cardEl.querySelector(`.cluster-viewport[data-cluster="${idx}"]`);
      const world = cardEl.querySelector(`.cluster-world[data-cluster="${idx}"]`);
      const svg = cardEl.querySelector(`.cluster-svg[data-cluster="${idx}"]`);
      const cardsLayer = cardEl.querySelector(`.cluster-cards-layer[data-cluster="${idx}"]`);
      if (!world || !svg || !cardsLayer) return;

      const cs = cluster.canvasState;
      world.style.transform = `translate(${cs.panX}px, ${cs.panY}px) scale(${cs.zoom})`;

      cardsLayer.innerHTML = '';
      Object.entries(cs.nodes).forEach(([tableName, node]) => {
        const color = this.colorForTable(tableName);
        const isIncluded = cluster.includedTables.has(tableName);
        const card = document.createElement('div');
        card.className = `cluster-table-card absolute rounded-xl bg-[#111826] border border-white/10 shadow-lg shadow-black/30 select-none ${isIncluded ? '' : 'opacity-40'}`;
        card.style.left = node.x + 'px';
        card.style.top = node.y + 'px';
        card.style.width = node.w + 'px';
        card.dataset.cluster = idx;
        card.dataset.table = tableName;

        card.innerHTML = `
          <div class="cluster-card-header h-8 rounded-t-xl flex items-center justify-between px-3 border-b border-white/10 cursor-grab active:cursor-grabbing" style="background: linear-gradient(180deg, ${color}26, transparent)">
            <div class="flex items-center gap-1.5 min-w-0">
              <span class="w-2 h-2 rounded-full shrink-0" style="background:${color}"></span>
              <span class="font-mono text-[12px] font-semibold text-white truncate">${this.escape(tableName)}</span>
            </div>
          </div>
          <div class="px-3 py-1.5 text-[11px] font-mono text-teal-300 flex items-center gap-1">
            <span class="text-slate-500">key:</span>
            <span class="truncate">${this.escape(node.col)}</span>
          </div>`;

        cardsLayer.appendChild(card);
      });

      this.redrawClusterSVG(idx);
    }

    redrawClusterSVG(idx) {
      const cluster = this.valueClusters && this.valueClusters[idx];
      if (!cluster) return;
      const cardEl = this.$.summaryBody.querySelector(`[data-cluster-card="${idx}"]`);
      if (!cardEl) return;
      const svg = cardEl.querySelector(`.cluster-svg[data-cluster="${idx}"]`);
      if (!svg) return;

      const cs = cluster.canvasState;
      svg.innerHTML = '';

      const seenEdge = new Set();
      cluster.edges.forEach(e => {
        const key = [e.fromTable, e.toTable].sort().join('-');
        if (seenEdge.has(key)) return;
        seenEdge.add(key);

        const n1 = cs.nodes[e.fromTable];
        const n2 = cs.nodes[e.toTable];
        if (!n1 || !n2) return;

        const x1 = n1.x + n1.w / 2;
        const y1 = n1.y + n1.h / 2;
        const x2 = n2.x + n2.w / 2;
        const y2 = n2.y + n2.h / 2;

        const dx = Math.max(Math.abs(x2 - x1) * 0.4, 30);
        const fromRight = x1 <= x2;
        const c1x = fromRight ? x1 + dx : x1 - dx;
        const c2x = fromRight ? x2 - dx : x2 + dx;

        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', `M ${x1} ${y1} C ${c1x} ${y1}, ${c2x} ${y2}, ${x2} ${y2}`);
        path.setAttribute('fill', 'none');
        path.setAttribute('stroke', '#5EEAD4');
        path.setAttribute('stroke-width', '1.8');
        path.setAttribute('stroke-dasharray', '4 4');
        path.setAttribute('stroke-opacity', '0.7');
        svg.appendChild(path);
      });
    }

    mountAllClusterCanvases() {
      if (!this.valueClusters) return;
      this.valueClusters.forEach((_, idx) => this.mountClusterCanvas(idx));
    }'''

    content = re.sub(old_render_svg_pattern, new_methods, content)

    # 2. Update renderClusterCard HTML to use renderClusterCanvasHtml
    content = content.replace(
        '<div class="rounded-lg bg-black/20 border border-white/5 p-2 mb-3">${this.renderClusterSVG(cluster)}</div>',
        '${this.renderClusterCanvasHtml(cluster, idx)}'
    )

    # 3. Update rerenderClusterCard to re-mount canvas after rerender
    content = content.replace(
        'if (wrapper) wrapper.outerHTML = this.renderClusterCard(cluster, idx);',
        'if (wrapper) { wrapper.outerHTML = this.renderClusterCard(cluster, idx); this.mountClusterCanvas(idx); }'
    )

    # 4. Update renderSummaryModal to call mountAllClusterCanvases
    content = content.replace(
        'this.$.summaryBody.innerHTML = `',
        'setTimeout(() => this.mountAllClusterCanvases(), 0);\n      this.$.summaryBody.innerHTML = `'
    )

    # 5. Add event listeners for cluster canvas dragging, panning, zooming in bindSummaryModal
    bind_modal_marker = "this.$.summaryBody.addEventListener('input', (e) => {"
    event_listeners_code = '''// Cluster Canvas Interactivity
      let activeClusterDrag = null;

      this.$.summaryBody.addEventListener('mousedown', (e) => {
        const header = e.target.closest('.cluster-card-header');
        if (header) {
          e.stopPropagation();
          const card = header.closest('.cluster-table-card');
          const idx = parseInt(card.dataset.cluster, 10);
          const tableName = card.dataset.table;
          const cluster = this.valueClusters && this.valueClusters[idx];
          if (!cluster) return;
          const cs = cluster.canvasState;
          const node = cs.nodes[tableName];
          activeClusterDrag = {
            type: 'card', idx, tableName, node,
            startMouseX: e.clientX, startMouseY: e.clientY,
            startX: node.x, startY: node.y, cs, card
          };
          header.classList.add('cursor-grabbing');
          return;
        }

        const viewport = e.target.closest('.cluster-viewport');
        if (viewport && !e.target.closest('.cluster-table-card') && !e.target.closest('button')) {
          const idx = parseInt(viewport.dataset.cluster, 10);
          const cluster = this.valueClusters && this.valueClusters[idx];
          if (!cluster) return;
          const cs = cluster.canvasState;
          activeClusterDrag = {
            type: 'pan', idx,
            startMouseX: e.clientX, startMouseY: e.clientY,
            startPanX: cs.panX, startPanY: cs.panY, cs, viewport
          };
          viewport.classList.add('cursor-grabbing');
        }
      });

      document.addEventListener('mousemove', (e) => {
        if (!activeClusterDrag) return;
        if (activeClusterDrag.type === 'card') {
          const { idx, node, startMouseX, startMouseY, startX, startY, cs, card } = activeClusterDrag;
          const dx = (e.clientX - startMouseX) / cs.zoom;
          const dy = (e.clientY - startMouseY) / cs.zoom;
          node.x = startX + dx;
          node.y = startY + dy;
          card.style.left = node.x + 'px';
          card.style.top = node.y + 'px';
          this.redrawClusterSVG(idx);
        } else if (activeClusterDrag.type === 'pan') {
          const { idx, startMouseX, startMouseY, startPanX, startPanY, cs, viewport } = activeClusterDrag;
          const dx = e.clientX - startMouseX;
          const dy = e.clientY - startMouseY;
          cs.panX = startPanX + dx;
          cs.panY = startPanY + dy;
          const world = viewport.querySelector(`.cluster-world[data-cluster="${idx}"]`);
          if (world) world.style.transform = `translate(${cs.panX}px, ${cs.panY}px) scale(${cs.zoom})`;
        }
      });

      document.addEventListener('mouseup', () => {
        if (activeClusterDrag) {
          if (activeClusterDrag.type === 'pan' && activeClusterDrag.viewport) {
            activeClusterDrag.viewport.classList.remove('cursor-grabbing');
          }
          activeClusterDrag = null;
        }
      });

      this.$.summaryBody.addEventListener('wheel', (e) => {
        const viewport = e.target.closest('.cluster-viewport');
        if (!viewport) return;
        e.preventDefault();
        const idx = parseInt(viewport.dataset.cluster, 10);
        const cluster = this.valueClusters && this.valueClusters[idx];
        if (!cluster) return;
        const cs = cluster.canvasState;
        const factor = e.deltaY > 0 ? 0.9 : 1.1;
        const newZoom = Math.min(2.5, Math.max(0.2, cs.zoom * factor));
        cs.zoom = newZoom;
        const world = viewport.querySelector(`.cluster-world[data-cluster="${idx}"]`);
        if (world) world.style.transform = `translate(${cs.panX}px, ${cs.panY}px) scale(${cs.zoom})`;
        const label = viewport.querySelector(`.cluster-zoom-label[data-cluster="${idx}"]`);
        if (label) label.textContent = Math.round(cs.zoom * 100) + '%';
      }, { passive: false });

      this.$.summaryBody.addEventListener('click', (e) => {
        const zOut = e.target.closest('.cluster-btn-zoom-out');
        const zIn = e.target.closest('.cluster-btn-zoom-in');
        const zFit = e.target.closest('.cluster-btn-fit');
        if (zOut || zIn || zFit) {
          const btn = zOut || zIn || zFit;
          const idx = parseInt(btn.dataset.cluster, 10);
          const cluster = this.valueClusters && this.valueClusters[idx];
          if (!cluster) return;
          const cs = cluster.canvasState;
          const cardEl = this.$.summaryBody.querySelector(`[data-cluster-card="${idx}"]`);
          const viewport = cardEl && cardEl.querySelector(`.cluster-viewport[data-cluster="${idx}"]`);
          const world = cardEl && cardEl.querySelector(`.cluster-world[data-cluster="${idx}"]`);
          if (!viewport || !world) return;

          if (zOut) cs.zoom = Math.max(0.2, cs.zoom / 1.2);
          else if (zIn) cs.zoom = Math.min(2.5, cs.zoom * 1.2);
          else if (zFit) {
            const nodesArr = Object.values(cs.nodes);
            if (nodesArr.length) {
              const minX = Math.min(...nodesArr.map(n => n.x));
              const minY = Math.min(...nodesArr.map(n => n.y));
              const maxX = Math.max(...nodesArr.map(n => n.x + n.w));
              const maxY = Math.max(...nodesArr.map(n => n.y + n.h));
              const bboxW = Math.max(maxX - minX, 1), bboxH = Math.max(maxY - minY, 1);
              const scale = Math.min(540 / bboxW, 240 / bboxH, 1.2);
              cs.zoom = Math.max(0.2, scale);
              cs.panX = (600 - bboxW * cs.zoom) / 2 - minX * cs.zoom;
              cs.panY = (280 - bboxH * cs.zoom) / 2 - minY * cs.zoom;
            }
          }

          world.style.transform = `translate(${cs.panX}px, ${cs.panY}px) scale(${cs.zoom})`;
          const label = viewport.querySelector(`.cluster-zoom-label[data-cluster="${idx}"]`);
          if (label) label.textContent = Math.round(cs.zoom * 100) + '%';
        }
      });\n\n      '''

    content = content.replace(bind_modal_marker, event_listeners_code + bind_modal_marker)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {file_path}")

update_erd(r"c:\Users\ASUS\Documents\Web Dev\tools\combine\toolsworks\public\tools\erd-visualizer.html")
update_erd(r"c:\Users\ASUS\Documents\Web Dev\tools\combine\erd-visualizer-Fixed.html")
