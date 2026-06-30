import { FileTerminal } from "lucide-react";

/**
 * Formats a Date object to a consistent, locale-stable string.
 * Example output: "30 Jun 2026, 01:10"
 * Uses en-GB explicitly so the format never varies by user's system locale.
 */
function formatReportDate(date) {
  return date.toLocaleString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
}

function ReportHeader({ analysisId, processing }) {
  const generatedAt = formatReportDate(new Date());

  return (
    <div className="card bg-base-100 shadow mb-6">
      <div className="card-body py-4">

        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">

          {/* ── Left: title block ── */}
          <div className="flex items-center gap-3">
            <FileTerminal size={22} className="text-primary shrink-0" />
            <div>
              <h1 className="text-xl font-bold text-base-content leading-tight">
                AI Boot Firmware &amp; OS Boot Analytics
              </h1>
              <p className="text-xs text-base-content/40 mt-0.5">
                Analysis Report · Generated {generatedAt}
              </p>
            </div>
          </div>

          {/* ── Right: metadata strip ── */}
          <div className="flex flex-wrap gap-x-6 gap-y-1 text-xs sm:text-right shrink-0">

            <div>
              <span className="text-base-content/40 uppercase tracking-wider font-mono">
                ID&nbsp;
              </span>
              <span className="font-mono text-base-content/70 break-all">
                {analysisId}
              </span>
            </div>

            <div>
              <span className="text-base-content/40 uppercase tracking-wider font-mono">
                Time&nbsp;
              </span>
              <span className="font-mono text-base-content/70">
                {processing.time}s
              </span>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}

export default ReportHeader;