'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';

export default function Home() {
  const tools = [
    {
      id: 'erd',
      title: 'ERD Visualizer',
      subtitle: 'Pemeta Skema & Relasi Database',
      description:
        'Visualisasikan file SQL skema database secara otomatis. Dilengkapi canvas interaktif (drag/zoom/pan), deteksi Foreign Key, pencocokan relasi data tersembunyi (Value Relation Engine), dan ringkasan relasi interaktif.',
      href: '/erd',
      color: 'from-teal-500/20 to-sky-500/10 border-teal-500/30 text-teal-400 hover:border-teal-400',
      badge: 'Interactive Canvas',
      badgeColor: 'bg-teal-400/10 text-teal-300 border-teal-400/30',
      icon: (
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <rect x="3" y="3" width="7" height="7" rx="1" />
          <rect x="14" y="3" width="7" height="7" rx="1" />
          <rect x="14" y="14" width="7" height="7" rx="1" />
          <rect x="3" y="14" width="7" height="7" rx="1" />
          <path d="M10 6.5h4M6.5 10v4M17.5 10v4M10 17.5h4" />
        </svg>
      ),
      features: ['Auto layout & force graph', 'Schema & value-based relations', 'Materialized View solver', 'Export JSON skema'],
    },
    {
      id: 'query-forge',
      title: 'QueryForge',
      subtitle: 'CSV to SQL INSERT Generator',
      description:
        'Ubah data CSV menjadi query INSERT SQL siap pakai. Tempel DDL CREATE TABLE, baca CSV (upload/paste), cocokkan kolom otomatis, auto-generate UUID/NOW(), serta pembatasan baris & batching query.',
      href: '/query-forge',
      color: 'from-lime-500/20 to-emerald-500/10 border-lime-500/30 text-lime-400 hover:border-lime-400',
      badge: 'SQL Generator',
      badgeColor: 'bg-lime-400/10 text-lime-300 border-lime-400/30',
      icon: (
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14 2 14 8 20 8" />
          <line x1="16" y1="13" x2="8" y2="13" />
          <line x1="16" y1="17" x2="8" y2="17" />
        </svg>
      ),
      features: ['Smart column auto-matching', 'Auto UUID() & NOW() injection', 'Per-batch query splitting', 'Cek duplikasi kolom otomatis'],
    },
    {
      id: 'data-bench',
      title: 'Data Bench',
      subtitle: 'Pembersih SQL & Excel ke CSV',
      description:
        'Dua panel utility praktis: Hapus seluruh komentar SQL (-- / # / /* */) & memadatkan baris kosong, atau konversi sheet Excel (.xlsx/.xls) menjadi CSV/ZIP dengan progres & sanitasi data.',
      href: '/data-bench',
      color: 'from-amber-500/20 to-orange-500/10 border-amber-500/30 text-amber-400 hover:border-amber-400',
      badge: 'SQL & Excel Tool',
      badgeColor: 'bg-amber-400/10 text-amber-300 border-amber-400/30',
      icon: (
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
          <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
          <line x1="12" y1="22.08" x2="12" y2="12" />
        </svg>
      ),
      features: ['SQL comment & whitespace stripper', 'Excel (.xlsx/.xls) to CSV parser', 'Multi-sheet ZIP export', 'Watchdog & chunk processing'],
    },
  ];

  return (
    <main className="relative min-h-[calc(100vh-3.5rem)] overflow-hidden px-4 py-12 sm:px-6 lg:px-8">
      {/* Background glow effects */}
      <div className="pointer-events-none absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute -top-40 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-gradient-to-tr from-teal-500/15 via-sky-500/10 to-transparent blur-3xl opacity-70" />
        <div className="absolute top-1/2 right-0 w-[500px] h-[500px] bg-amber-500/5 blur-3xl" />
      </div>

      <div className="mx-auto max-w-6xl">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <div className="inline-flex items-center gap-2 rounded-full border border-teal-400/30 bg-teal-400/10 px-3.5 py-1 font-mono text-xs text-teal-300 mb-6">
            <span>⚡ Suite Tool Developer Terpadu</span>
          </div>

          <h1 className="font-mono text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white mb-6">
            toolsworks<span className="text-teal-400">.dev</span>
          </h1>

          <p className="mx-auto max-w-2xl text-base sm:text-lg text-slate-400 leading-relaxed">
            Semua kebutuhan analisis database, pembuatan query INSERT SQL dari CSV, hingga pembersihan SQL &amp; konversi Excel — diproses <span className="text-white font-medium">100% lokal</span> langsung di browser Anda.
          </p>
        </motion.div>

        {/* Grid Tools */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {tools.map((tool, idx) => (
            <motion.div
              key={tool.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: idx * 0.15 }}
            >
              <Link
                href={tool.href}
                className={`group relative flex flex-col h-full rounded-2xl border bg-gradient-to-b ${tool.color} p-6 transition-all duration-200 hover:-translate-y-1 hover:shadow-xl hover:shadow-black/50`}
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="p-3 rounded-xl bg-black/40 border border-white/10 text-white">
                    {tool.icon}
                  </div>
                  <span className={`font-mono text-[11px] px-2.5 py-1 rounded-md border ${tool.badgeColor}`}>
                    {tool.badge}
                  </span>
                </div>

                <h2 className="font-mono text-xl font-bold text-white mb-1 group-hover:text-teal-300 transition-colors">
                  {tool.title}
                </h2>
                <p className="font-mono text-xs text-slate-400 mb-3 font-semibold">
                  {tool.subtitle}
                </p>
                <p className="text-xs text-slate-300/80 leading-relaxed mb-6 flex-1">
                  {tool.description}
                </p>

                <div className="border-t border-white/10 pt-4 space-y-2">
                  {tool.features.map((feat, fIdx) => (
                    <div key={fIdx} className="flex items-center gap-2 text-[11px] text-slate-400">
                      <span className="w-1.5 h-1.5 rounded-full bg-slate-500 group-hover:bg-teal-400 transition-colors" />
                      <span>{feat}</span>
                    </div>
                  ))}
                </div>

                <div className="mt-6 flex items-center gap-1.5 font-mono text-xs font-semibold text-white group-hover:translate-x-1 transition-transform">
                  <span>Buka Tool</span>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>

        {/* Footer info */}
        <footer className="mt-16 text-center text-xs text-slate-600 font-mono">
          toolsworks.dev — Privasi terjamin, tidak ada data file yang diunggah ke server manapun.
        </footer>
      </div>
    </main>
  );
}
