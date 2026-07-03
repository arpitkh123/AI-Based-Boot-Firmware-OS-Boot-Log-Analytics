import { Activity, ShieldAlert, Cpu, HardDrive, Wifi, Radio } from "lucide-react";

function SubsystemDistribution({ severitySummary, subsystemSummary }) {
  const severities = severitySummary || {};
  const subsystems = subsystemSummary || {};

  const totalLogs = Object.values(subsystems).reduce((a, b) => a + b, 0) || 1;

  // Icons mapper for subsystems
  const getSubsystemIcon = (sub) => {
    switch (sub) {
      case "BOOT": return <Radio size={14} className="text-primary shrink-0" />;
      case "KERNEL": return <Cpu size={14} className="text-secondary shrink-0" />;
      case "MEMORY": return <Activity size={14} className="text-accent shrink-0" />;
      case "FILESYSTEM": return <HardDrive size={14} className="text-info shrink-0" />;
      case "USB": return <ShieldAlert size={14} className="text-warning shrink-0" />;
      case "NETWORK": return <Wifi size={14} className="text-success shrink-0" />;
      default: return <Activity size={14} className="text-base-content/40 shrink-0" />;
    }
  };

  const getSubsystemBadgeClass = (sub) => {
    switch (sub) {
      case "BOOT": return "badge-primary bg-primary/10 text-primary border-primary/20";
      case "KERNEL": return "badge-secondary bg-secondary/10 text-secondary border-secondary/20";
      case "MEMORY": return "badge-accent bg-accent/10 text-accent border-accent/20";
      case "FILESYSTEM": return "badge-info bg-info/10 text-info border-info/20";
      case "USB": return "badge-warning bg-warning/10 text-warning border-warning/20";
      case "NETWORK": return "badge-success bg-success/10 text-success border-success/20";
      default: return "badge-ghost opacity-60";
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-6">
      
      {/* ── Left Column: Severity Summary ── */}
      <div className="lg:col-span-5 card bg-base-100 shadow border border-base-300">
        <div className="card-body">
          <h3 className="card-title text-base font-bold text-base-content mb-3">
            Severity Summary Indicators
          </h3>

          <div className="space-y-3">
            {/* ERROR */}
            <div>
              <div className="flex justify-between items-center text-xs font-mono mb-1">
                <span className="text-error font-bold">ERROR</span>
                <span className="text-error font-bold">{severities.ERROR || 0}</span>
              </div>
              <progress className="progress progress-error w-full h-2 bg-error/10" value={severities.ERROR || 0} max={totalLogs} />
            </div>

            {/* WARNING */}
            <div>
              <div className="flex justify-between items-center text-xs font-mono mb-1">
                <span className="text-warning font-bold">WARNING</span>
                <span className="text-warning font-bold">{severities.WARNING || 0}</span>
              </div>
              <progress className="progress progress-warning w-full h-2 bg-warning/10" value={severities.WARNING || 0} max={totalLogs} />
            </div>

            {/* SUCCESS */}
            <div>
              <div className="flex justify-between items-center text-xs font-mono mb-1">
                <span className="text-success font-bold">SUCCESS</span>
                <span className="text-success font-bold">{severities.SUCCESS || 0}</span>
              </div>
              <progress className="progress progress-success w-full h-2 bg-success/10" value={severities.SUCCESS || 0} max={totalLogs} />
            </div>

            {/* INFO */}
            <div>
              <div className="flex justify-between items-center text-xs font-mono mb-1">
                <span className="text-neutral-content/60 font-semibold">INFO</span>
                <span className="text-neutral-content/60 font-semibold">{severities.INFO || 0}</span>
              </div>
              <progress className="progress progress-neutral w-full h-2 bg-base-300" value={severities.INFO || 0} max={totalLogs} />
            </div>
          </div>
        </div>
      </div>

      {/* ── Right Column: Subsystem Summary ── */}
      <div className="lg:col-span-7 card bg-base-100 shadow border border-base-300">
        <div className="card-body">
          <h3 className="card-title text-base font-bold text-base-content mb-3">
            Subsystem Distribution
          </h3>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {Object.entries(subsystems).map(([sub, count]) => {
              const percentage = Math.round((count / totalLogs) * 100);
              return (
                <div key={sub} className="p-3 bg-base-200/40 border border-base-300/60 rounded-xl flex items-center justify-between gap-3 min-w-0">
                  <div className="flex items-center gap-2 min-w-0">
                    {getSubsystemIcon(sub)}
                    <span className="text-[11px] font-mono font-bold uppercase truncate text-base-content/80">
                      {sub}
                    </span>
                  </div>
                  <div className="text-right shrink-0">
                    <span className="text-xs font-bold text-base-content block">{count}</span>
                    <span className="text-[9px] text-base-content/40 font-mono block">{percentage}%</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

    </div>
  );
}

export default SubsystemDistribution;
