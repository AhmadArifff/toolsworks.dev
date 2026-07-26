'use client';

export default function DataBenchPage() {
  return (
    <div className="w-full h-[calc(100vh-3.5rem)] overflow-hidden bg-[#0D1117]">
      <iframe
        src="/tools/data-bench.html"
        title="Data Bench — Pembersih SQL & Excel ke CSV"
        className="w-full h-full border-0"
      />
    </div>
  );
}
