'use client';

export default function QueryForgePage() {
  return (
    <div className="w-full h-[calc(100vh-3.5rem)] overflow-hidden bg-[#0a0b0d]">
      <iframe
        src="/tools/sql-insert-generator.html"
        title="QueryForge — SQL Insert Generator"
        className="w-full h-full border-0"
      />
    </div>
  );
}
