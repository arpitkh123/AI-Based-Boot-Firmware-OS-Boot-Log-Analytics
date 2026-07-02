import { CheckCircle2, XCircle } from "lucide-react";

/**
 * A single label → value row used inside detail cards.
 * Keeps a consistent two-column layout across all info cards.
 */
function InfoRow({ label, value, mono = false }) {
  return (
    <div className="flex items-start py-2.5 gap-4">
      <span className="text-xs font-mono uppercase tracking-wider text-base-content/40 w-36 shrink-0 pt-0.5">
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

function BootSummaryCard({ boot, details }) {
  const statusIcon = boot.bootSuccessful ? (
    <CheckCircle2 size={14} className="text-success inline mr-1 mb-0.5" />
  ) : (
    <XCircle size={14} className="text-error inline mr-1 mb-0.5" />
  );

  const statusText = boot.bootSuccessful ? "Successful" : "Failed";
  const statusColor = boot.bootSuccessful ? "text-success" : "text-error";

  // Check if we have duration in ms or s
  const durationVal = typeof boot.bootDuration === "number" && boot.bootDuration < 100 
    ? `${(boot.bootDuration * 1000).toFixed(0)} ms (${boot.bootDuration.toFixed(3)} s)` 
    : `${boot.bootDuration} s`;

  return (
    <div className="card bg-base-100 shadow h-full border border-base-300">
      <div className="card-body pb-4">

        <h2 className="card-title text-base mb-1 font-bold text-base-content">
          Boot Summary
        </h2>

        <div className="divide-y divide-base-300">
          {/* Status */}
          <div className="flex items-start py-2.5 gap-4">
            <span className="text-xs font-mono uppercase tracking-wider text-base-content/40 w-36 shrink-0 pt-0.5">
              Status
            </span>
            <span className={`text-sm font-semibold flex items-center ${statusColor}`}>
              {statusIcon}
              {statusText}
            </span>
          </div>

          {/* Failure Stage */}
          <InfoRow
            label="Failure Stage"
            value={boot.failureStage ?? "—"}
          />

          {/* Duration */}
          <InfoRow
            label="Boot Duration"
            value={durationVal}
            mono
          />

          {/* Boot Type */}
          <InfoRow
            label="Boot Type / Source"
            value={details?.bootSource || "Raw UART"}
          />
        </div>

      </div>
    </div>
  );
}

export default BootSummaryCard;