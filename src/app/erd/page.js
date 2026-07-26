'use client';

export default function ERDPage() {
  return (
    <div className="w-full h-[calc(100vh-3.5rem)] overflow-hidden bg-[#0A0E14]">
      <iframe
        src="/tools/erd-visualizer.html"
        title="ERD Visualizer"
        className="w-full h-full border-0"
      />
    </div>
  );
}
