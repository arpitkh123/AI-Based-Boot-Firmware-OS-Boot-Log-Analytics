import { useLocation } from "react-router-dom";
import { CheckCircle2, Circle, LoaderCircle, Cpu } from "lucide-react";
import PageTransition from "../../components/shared/PageTransition";

import { useAnalysis } from "../../hooks/useAnalysis";
import { PROCESSING_STEPS } from "../../constants/steps";

function Processing() {
  const location = useLocation();
  const fileName = location.state?.file?.name ?? "boot.log";

  const { currentStep, totalSteps } = useAnalysis();

  const progressPercent = Math.round((currentStep / totalSteps) * 100);

  return (
    <PageTransition>
      <div className="min-h-[calc(100vh-80px)] bg-base-200 flex items-center justify-center p-4 lg:p-8">
        <div className="card bg-base-100 shadow-xl w-full max-w-2xl overflow-hidden">
          <div className="card-body gap-6 p-8 lg:p-12">

            {/* ── Header ── */}
            <div className="text-center">
              <div className="flex items-center justify-center gap-2 mb-3">
                <Cpu size={22} className="text-primary animate-pulse" />
                <span className="text-xs font-mono tracking-widest text-base-content/40 uppercase">
                  Running Diagnostics Pipeline
                </span>
              </div>

              <h1 className="text-3xl font-extrabold tracking-tight text-base-content">
                Analyzing Boot Log
              </h1>

              <p
                className="text-xs text-base-content/50 mt-2 font-mono truncate max-w-md mx-auto bg-base-200 px-3 py-1.5 rounded-lg border border-base-300"
                title={fileName}
              >
                {fileName}
              </p>
            </div>

            {/* ── Progress Bar ── */}
            <div className="space-y-2 bg-base-200/30 p-4 rounded-xl border border-base-300/50">
              <div className="flex justify-between items-center">
                <span className="text-xs text-base-content/60 font-semibold uppercase tracking-wider font-mono">
                  Overall Progress
                </span>
                <span className="text-xs font-mono text-primary font-bold">
                  {progressPercent}%
                </span>
              </div>
              <progress
                id="analysis-progress"
                className="progress progress-primary w-full h-3"
                value={progressPercent}
                max="100"
              />
            </div>

            {/* ── Step List ── */}
            <div className="space-y-4 py-2">
              {PROCESSING_STEPS.map((step, index) => {
                const isDone = index < currentStep;
                const isActive = index === currentStep;

                return (
                  <div
                    key={step}
                    className={`flex items-center gap-4 p-3 rounded-lg border transition-all duration-300 ${
                      isActive
                        ? "bg-base-200 border-primary/30 shadow-sm"
                        : isDone
                        ? "bg-base-200/20 border-transparent opacity-60"
                        : "bg-transparent border-transparent"
                    }`}
                  >
                    {/* Step icon */}
                    <div className="shrink-0 w-6 flex justify-center">
                      {isDone ? (
                        <CheckCircle2
                          size={20}
                          className="text-success"
                        />
                      ) : isActive ? (
                        <LoaderCircle
                          size={20}
                          className="animate-spin text-primary"
                        />
                      ) : (
                        <Circle
                          size={20}
                          className="text-base-content/20"
                        />
                      )}
                    </div>

                    {/* Step label */}
                    <span
                      className={[
                        "text-sm transition-all duration-300 flex-1 min-w-0 truncate",
                        isDone
                          ? "text-base-content/50 line-through decoration-base-content/20"
                          : isActive
                          ? "text-base-content font-bold"
                          : "text-base-content/25",
                      ].join(" ")}
                    >
                      {step}
                    </span>

                    {/* Done badge */}
                    {isDone && (
                      <span className="badge badge-success badge-outline badge-xs font-mono px-2 py-1 uppercase tracking-wider text-[9px]">
                        done
                      </span>
                    )}
                  </div>
                );
              })}
            </div>

            <div className="divider my-0 border-base-300" />

            <p className="text-center text-xs text-base-content/40 font-medium">
              Please keep this browser window open while the diagnostic analysis is completed.
            </p>

          </div>
        </div>
      </div>
    </PageTransition>
  );
}

export default Processing;