import { ShieldCheck, ShieldAlert, ShieldQuestion } from "lucide-react";

const CONFIDENCE_HIGH = 80;

/**
 * Returns Tailwind color class and status metadata based on boot outcome + confidence.
 * Used for both the radial-progress ring and the status icon.
 */
function getStatusMeta(bootStatus, confidence) {
  if (bootStatus && confidence >= CONFIDENCE_HIGH) {
    return {
      ringColor: "text-success",
      iconColor: "text-success",
      Icon: ShieldCheck,
      label: "BOOT SUCCESSFUL",
      badgeClass: "badge-success",
    };
  }

  if (!bootStatus && confidence >= CONFIDENCE_HIGH) {
    return {
      ringColor: "text-error",
      iconColor: "text-error",
      Icon: ShieldAlert,
      label: "BOOT FAILED",
      badgeClass: "badge-error",
    };
  }

  // Low confidence — uncertain prediction regardless of outcome
  return {
    ringColor: "text-warning",
    iconColor: "text-warning",
    Icon: ShieldQuestion,
    label: bootStatus ? "BOOT SUCCESSFUL" : "BOOT FAILED",
    badgeClass: bootStatus ? "badge-success" : "badge-error",
  };
}

function PredictionCard({ prediction, bootStatus }) {
  const { ringColor, iconColor, Icon, label, badgeClass } =
    getStatusMeta(bootStatus, prediction.confidence);

  return (
    <div className="card bg-base-100 shadow mb-6">
      <div className="card-body">

        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-6">

          {/* ── Left: class + boot status ── */}
          <div className="flex items-start gap-4">

            {/* Status icon */}
            <div className={`mt-1 shrink-0 ${iconColor}`}>
              <Icon size={36} strokeWidth={1.5} />
            </div>

            <div>
              {/* Section label */}
              <p className="text-xs font-mono uppercase tracking-widest text-base-content/40 mb-1">
                ML Prediction
              </p>

              {/* Prediction class — h2 since h1 is in ReportHeader */}
              <h2 className="text-4xl font-bold tracking-tight text-base-content">
                {prediction.class}
              </h2>

              {/* Boot status badge */}
              <div className="mt-3">
                <span className={`badge ${badgeClass} badge-lg font-semibold`}>
                  {label}
                </span>
              </div>
            </div>

          </div>

          {/* ── Right: confidence ring ── */}
          <div className="flex flex-col items-center gap-2 shrink-0">
            <div
              className={`radial-progress font-bold text-sm ${ringColor}`}
              style={{
                "--value": prediction.confidence,
                "--size": "6rem",
                "--thickness": "6px",
              }}
              role="progressbar"
              aria-label={`Model confidence: ${prediction.confidence}%`}
              aria-valuenow={prediction.confidence}
              aria-valuemin={0}
              aria-valuemax={100}
            >
              {prediction.confidence}%
            </div>
            <p className="text-xs text-base-content/50 font-medium tracking-wide uppercase">
              Confidence
            </p>
            {prediction.confidence < CONFIDENCE_HIGH && (
              <span className="badge badge-warning badge-sm">Low Confidence</span>
            )}
          </div>

        </div>

      </div>
    </div>
  );
}

export default PredictionCard;