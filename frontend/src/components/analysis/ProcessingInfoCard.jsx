/**
 * InfoRow — consistent label → value row for detail cards.
 * Identical pattern to BootSummaryCard's InfoRow.
 * If these cards grow significantly, promote InfoRow to components/shared/.
 */
function InfoRow({ label, value, mono = false }) {
  return (
    <div className="flex items-start py-2.5 gap-4">
      <span className="text-xs font-mono uppercase tracking-wider text-base-content/40 w-32 shrink-0 pt-0.5">
        {label}
      </span>
      <span
        className={`text-sm text-base-content font-medium break-all ${
          mono ? "font-mono" : ""
        }`}
      >
        {value}
      </span>
    </div>
  );
}

function ProcessingInfoCard({ processing, statistics, analysisId }) {
  return (
    <div className="card bg-base-100 shadow h-full">
      <div className="card-body pb-4">

        <h2 className="card-title text-base mb-1">
          Processing Metadata
        </h2>

        <div className="divide-y divide-base-300">
          <InfoRow
            label="Analysis ID"
            value={analysisId}
            mono
          />
          <InfoRow
            label="Time Taken"
            value={`${processing.time} s`}
            mono
          />
          <InfoRow
            label="Logs Parsed"
            value={statistics.logsParsed}
            mono
          />
        </div>

      </div>
    </div>
  );
}

export default ProcessingInfoCard;