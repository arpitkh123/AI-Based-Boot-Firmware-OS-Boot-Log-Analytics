/**
 * InfoRow — consistent label → value row for detail cards.
 * Identical pattern to BootSummaryCard's InfoRow.
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

function ProcessingInfoCard({ processing, statistics, analysisId, details }) {
  // Format file size
  const formatBytes = (bytes) => {
    if (!bytes) return "0 B";
    const k = 1024;
    const sizes = ["B", "KB", "MB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  const fileSizeStr = details?.fileSizeBytes ? formatBytes(details.fileSizeBytes) : "Unknown Size";

  return (
    <div className="card bg-base-100 shadow h-full border border-base-300">
      <div className="card-body pb-4">

        <h2 className="card-title text-base mb-1 font-bold text-base-content">
          Log Properties &amp; Metadata
        </h2>

        <div className="divide-y divide-base-300">
          <InfoRow
            label="Analysis ID"
            value={analysisId}
            mono
          />
          <InfoRow
            label="Hardware Model"
            value={details?.machineModel || "Generic Platform"}
          />
          <InfoRow
            label="Linux Version"
            value={details?.linuxVersion || "N/A"}
          />
          <InfoRow
            label="File Name"
            value={details?.filename || "boot.log"}
          />
          <InfoRow
            label="File Size"
            value={fileSizeStr}
            mono
          />
        </div>

      </div>
    </div>
  );
}

export default ProcessingInfoCard;