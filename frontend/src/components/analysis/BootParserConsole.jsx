import { CheckCircle2, XCircle, ChevronRight, Terminal, AlertTriangle } from "lucide-react";

function BootParserConsole({ boot }) {
  const progress = boot.bootProgress || {};
  const failures = boot.failures || {};

  // Ordered boot stages sequence
  const steps = [
    { key: "kernelStarted", label: "Kernel Initialization Started" },
    { key: "rootfsMounted", label: "Root Filesystem Mounted (RootFS)" },
    { key: "initStarted", label: "Init User-space Process Launched" },
    { key: "loginPromptDetected", label: "Login Prompt Spawned" },
    { key: "bootSuccessful", label: "Boot Sequence Completed Successfully" }
  ];

  // Specific boot subsystem failures
  const failureLabels = [
    { key: "kernelPanic", label: "Kernel Panic" },
    { key: "irqFailure", label: "IRQ Interrupt Fault" },
    { key: "dmaFailure", label: "DMA Allocation Failure" },
    { key: "rootfsFailure", label: "RootFS Mounting Fault" },
    { key: "dtbFailure", label: "DeviceTree Overlay Fault" },
    { key: "oomDetected", label: "Out Of Memory (OOM Kill)" },
    { key: "cpuFailure", label: "CPU Secondary Core Fault" },
    { key: "filesystemFailure", label: "Filesystem Corruption" },
    { key: "initFailure", label: "Init Spawn Failure" }
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-6">
      
      {/* ── Left Column: Boot Stage Timeline ── */}
      <div className="lg:col-span-6 card bg-base-100 shadow border border-base-300">
        <div className="card-body">
          <h3 className="card-title text-base font-bold text-base-content mb-3 flex items-center gap-2">
            <ChevronRight size={18} className="text-primary" />
            Boot Sequence Timeline
          </h3>

          <div className="space-y-4 relative before:absolute before:left-3 before:top-2 before:bottom-2 before:w-[2px] before:bg-base-300">
            {steps.map((step) => {
              const active = progress[step.key];
              return (
                <div key={step.key} className="flex items-center gap-3 relative pl-6">
                  {/* Status indicator bullet */}
                  <div className={`absolute left-1.5 w-3.5 h-3.5 rounded-full border-2 -translate-x-1/2 flex items-center justify-center transition-colors duration-200 ${
                    active 
                      ? "bg-success border-success text-success-content" 
                      : "bg-base-100 border-base-300"
                  }`}>
                    {active && <div className="w-1 h-1 bg-white rounded-full" />}
                  </div>
                  
                  <span className={`text-xs font-mono font-medium ${
                    active ? "text-base-content font-bold" : "text-base-content/30"
                  }`}>
                    {step.label}
                  </span>
                  
                  {active ? (
                    <span className="badge badge-success badge-outline badge-xs text-[9px] font-semibold py-1">PASSED</span>
                  ) : (
                    <span className="badge badge-ghost badge-outline badge-xs text-[9px] opacity-40 py-1">PENDING</span>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* ── Right Column: Subsystem Failures Matrix ── */}
      <div className="lg:col-span-6 card bg-base-100 shadow border border-base-300">
        <div className="card-body">
          <h3 className="card-title text-base font-bold text-base-content mb-3 flex items-center gap-2">
            <AlertTriangle size={16} className="text-warning" />
            Subsystem Health Diagnostics
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            {failureLabels.map((f) => {
              const triggered = failures[f.key];
              return (
                <div 
                  key={f.key} 
                  className={`p-2.5 border rounded-lg flex items-center justify-between text-xs font-mono transition-all duration-200 ${
                    triggered 
                      ? "bg-error/15 border-error/35 text-error font-bold" 
                      : "bg-base-200/40 border-base-300/60 text-base-content/60"
                  }`}
                >
                  <span className="truncate pr-2">{f.label}</span>
                  <span className={`badge badge-xs font-semibold px-2 py-1 shrink-0 ${
                    triggered ? "badge-error" : "badge-neutral opacity-50"
                  }`}>
                    {triggered ? "TRIGGERED" : "OK"}
                  </span>
                </div>
              );
            })}
          </div>

          {/* Core Boot Error Details Block */}
          {!boot.bootSuccessful && (boot.failureType || boot.failureReason) && (
            <div className="mt-4 p-3 bg-error/10 border border-error/20 rounded-xl space-y-2">
              <div className="flex items-center gap-2 text-xs font-bold text-error">
                <Terminal size={14} />
                <span>Primary Failure Source: {boot.failureType || "CRITICAL_ERROR"}</span>
              </div>
              <p className="text-xs text-base-content/80 leading-relaxed font-semibold">
                {boot.failureReason}
              </p>
              {boot.failureLog && (
                <div className="bg-neutral-950 p-2 rounded text-[10px] text-error font-mono break-all whitespace-pre-wrap max-h-24 overflow-y-auto border border-error/25">
                  {boot.failureLog}
                </div>
              )}
            </div>
          )}
        </div>
      </div>

    </div>
  );
}

export default BootParserConsole;
