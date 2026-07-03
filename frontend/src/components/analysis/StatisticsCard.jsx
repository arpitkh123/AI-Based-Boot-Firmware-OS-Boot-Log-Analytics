import {
  FileText,
  CircleX,
  TriangleAlert,
  Clock,
  Percent,
} from "lucide-react";

/**
 * A single stat cell — keeps the stat markup DRY.
 */
function StatCell({ icon: Icon, iconClass = "", value, valueClass = "", label, desc }) {
  return (
    <div className="stat">
      <div className={`stat-figure ${iconClass}`}>
        <Icon size={20} />
      </div>
      <div className={`stat-value text-2xl ${valueClass}`}>
        {value}
      </div>
      <div className="stat-title text-xs">
        {label}
      </div>
      {desc && (
        <div className="stat-desc text-[10px] opacity-60">
          {desc}
        </div>
      )}
    </div>
  );
}

function StatisticsCard({ statistics }) {
  const total = statistics.totalLines || statistics.logsParsed || 100;
  const parsed = statistics.logsParsed || 100;
  const successRatio = total > 0 ? Math.round((parsed / total) * 100) : 100;

  return (
    <div className="stats stats-vertical lg:stats-horizontal shadow w-full mb-6 border border-base-300">

      <StatCell
        icon={FileText}
        value={total}
        label="Total Log Lines"
        desc={`${parsed} parsed successfully`}
      />

      <StatCell
        icon={Percent}
        value={`${successRatio}%`}
        label="Parsing Quality"
        desc={`${statistics.ignoredLines || 0} lines ignored`}
      />

      <StatCell
        icon={CircleX}
        iconClass="text-error"
        value={statistics.errors}
        valueClass="text-error"
        label="Errors Detected"
        desc="Critical register panics"
      />

      <StatCell
        icon={TriangleAlert}
        iconClass="text-warning"
        value={statistics.warnings}
        valueClass="text-warning"
        label="Warnings Flagged"
        desc="Subsystem delay flags"
      />

      <StatCell
        icon={Clock}
        value={`${statistics.templates || 0}`}
        label="Mined Clusters"
        desc="Sequential template logs"
      />

    </div>
  );
}

export default StatisticsCard;