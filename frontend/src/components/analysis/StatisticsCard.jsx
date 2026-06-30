import {
  FileText,
  CircleX,
  TriangleAlert,
  Blocks,
  Brain,
} from "lucide-react";

/**
 * A single stat cell — keeps the stat markup DRY.
 */
function StatCell({ icon: Icon, iconClass = "", value, valueClass = "", label }) {
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
    </div>
  );
}

function StatisticsCard({ statistics }) {
  return (
    <div className="stats stats-vertical lg:stats-horizontal shadow w-full mb-6">

      <StatCell
        icon={FileText}
        value={statistics.logsParsed}
        label="Logs Parsed"
      />

      <StatCell
        icon={CircleX}
        iconClass="text-error"
        value={statistics.errors}
        valueClass="text-error"
        label="Errors"
      />

      <StatCell
        icon={TriangleAlert}
        iconClass="text-warning"
        value={statistics.warnings}
        valueClass="text-warning"
        label="Warnings"
      />

      <StatCell
        icon={Blocks}
        value={statistics.templates}
        label="Templates"
      />

      <StatCell
        icon={Brain}
        value={statistics.features}
        label="Features"
      />

    </div>
  );
}

export default StatisticsCard;