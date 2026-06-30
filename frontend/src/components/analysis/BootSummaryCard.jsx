import { CheckCircle2, XCircle } from "lucide-react";

/**
 * A single label → value row used inside detail cards.
 * Keeps a consistent two-column layout across all info cards.
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

function BootSummaryCard({ boot }) {
  const statusIcon = boot.bootSuccessful ? (
    <CheckCircle2 size={14} className="text-success inline mr-1 mb-0.5" />
  ) : (
    <XCircle size={14} className="text-error inline mr-1 mb-0.5" />
  );

  const statusText = boot.bootSuccessful ? "Successful" : "Failed";
  const statusColor = boot.bootSuccessful ? "text-success" : "text-error";

  return (
    <div className="card bg-base-100 shadow h-full">
      <div className="card-body pb-4">

        <h2 className="card-title text-base mb-1">
          Boot Summary
        </h2>

        <div className="divide-y divide-base-300">
          {/* Status */}
          <div className="flex items-start py-2.5 gap-4">
            <span className="text-xs font-mono uppercase tracking-wider text-base-content/40 w-32 shrink-0 pt-0.5">
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
            label="Duration"
            value={`${boot.bootDuration} ms`}
            mono
          />
        </div>

      </div>
    </div>
  );
}

export default BootSummaryCard;