import { useState } from "react";
import { Search, ListFilter, AlertCircle, AlertTriangle, Info, Terminal } from "lucide-react";

function LogTimelineInspector({ timeline }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [severityFilter, setSeverityFilter] = useState("ALL");
  const [subsystemFilter, setSubsystemFilter] = useState("ALL");
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 50;

  if (!timeline || timeline.length === 0) {
    return (
      <div className="card bg-base-100 shadow border border-base-300 p-8 text-center text-base-content/40">
        <Terminal size={32} className="mx-auto mb-2 opacity-55" />
        <p className="text-xs font-mono">No sequence timeline data parsed from log.</p>
      </div>
    );
  }

  // Get subsystems list
  const subsystems = ["ALL", ...new Set(timeline.map(item => item.subsystem).filter(Boolean))];

  // Filtering logs
  const filteredTimeline = timeline.filter(item => {
    const matchesSearch = item.message.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          (item.subsystem && item.subsystem.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesSeverity = severityFilter === "ALL" || item.severity === severityFilter;
    const matchesSubsystem = subsystemFilter === "ALL" || item.subsystem === subsystemFilter;

    return matchesSearch && matchesSeverity && matchesSubsystem;
  });

  // Pagination logic
  const totalPages = Math.ceil(filteredTimeline.length / itemsPerPage);
  const paginatedTimeline = filteredTimeline.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const getSeverityBadgeClass = (severity) => {
    switch (severity) {
      case "ERROR":
        return "badge-error bg-error/15 text-error border-error/20";
      case "WARNING":
        return "badge-warning bg-warning/15 text-warning border-warning/20";
      case "SUCCESS":
        return "badge-success bg-success/15 text-success border-success/20";
      default:
        return "badge-ghost opacity-60";
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case "ERROR":
        return <AlertCircle size={12} className="shrink-0" />;
      case "WARNING":
        return <AlertTriangle size={12} className="shrink-0" />;
      default:
        return <Info size={12} className="shrink-0" />;
    }
  };

  return (
    <div className="card bg-base-100 shadow border border-base-300 overflow-hidden mb-6 no-print">
      <div className="card-body p-6 gap-4">
        
        {/* Title & Filters */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-base-300 pb-4">
          <div>
            <h2 className="card-title text-base font-bold text-base-content flex items-center gap-2">
              <Terminal size={18} className="text-primary" />
              Interactive Boot Timeline Inspector
            </h2>
            <p className="text-[11px] text-base-content/50">
              Browse sequenced boot segments, filter logs by subsystem alerts, and examine timestamp progressions.
            </p>
          </div>

          <div className="flex flex-wrap gap-2 w-full md:w-auto">
            {/* Search Input */}
            <div className="relative flex-1 md:w-60 min-w-[200px]">
              <Search className="absolute left-2.5 top-2 text-base-content/40" size={14} />
              <input
                type="text"
                placeholder="Search log messages..."
                className="input input-xs input-bordered pl-8 w-full rounded-md text-xs"
                value={searchTerm}
                onChange={(e) => {
                  setSearchTerm(e.target.value);
                  setCurrentPage(1);
                }}
              />
            </div>
          </div>
        </div>

        {/* Filters Panel */}
        <div className="flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex flex-wrap items-center gap-2">
            <span className="font-mono text-[10px] text-base-content/40 uppercase">Severity:</span>
            {["ALL", "INFO", "WARNING", "ERROR"].map((sev) => (
              <button
                key={sev}
                onClick={() => {
                  setSeverityFilter(sev);
                  setCurrentPage(1);
                }}
                className={`btn btn-xs rounded-md font-mono ${
                  severityFilter === sev 
                    ? "btn-primary font-bold" 
                    : "btn-ghost border border-base-300"
                }`}
              >
                {sev}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-2">
            <span className="font-mono text-[10px] text-base-content/40 uppercase">Subsystem:</span>
            <select
              className="select select-xs select-bordered rounded-md text-xs font-mono"
              value={subsystemFilter}
              onChange={(e) => {
                setSubsystemFilter(e.target.value);
                setCurrentPage(1);
              }}
            >
              {subsystems.map(sub => (
                <option key={sub} value={sub}>{sub}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Logs Table Container */}
        <div className="overflow-x-auto border border-base-300 rounded-lg max-h-[420px] overflow-y-auto">
          <table className="table table-xs table-pin-rows table-pin-cols w-full">
            <thead>
              <tr className="bg-base-200 text-base-content/60 font-mono text-[10px] uppercase border-b border-base-300">
                <th className="w-16 text-center">Line</th>
                <th className="w-24">Time (s)</th>
                <th className="w-24 text-center">Severity</th>
                <th className="w-28">Subsystem</th>
                <th>Log Message</th>
              </tr>
            </thead>
            <tbody>
              {paginatedTimeline.length > 0 ? (
                paginatedTimeline.map((item) => (
                  <tr key={item.line} className="hover:bg-base-200/40 font-mono text-[11px] transition-colors border-b border-base-200">
                    <td className="text-center opacity-40 font-semibold">{item.line}</td>
                    <td className="text-primary font-semibold">
                      {item.timestamp !== null ? item.timestamp.toFixed(6) : "—"}
                    </td>
                    <td className="text-center">
                      <span className={`badge badge-xs gap-1 py-1 font-semibold ${getSeverityBadgeClass(item.severity)}`}>
                        {getSeverityIcon(item.severity)}
                        {item.severity}
                      </span>
                    </td>
                    <td>
                      <span className="badge badge-neutral badge-xs font-mono">{item.subsystem || "UNKNOWN"}</span>
                    </td>
                    <td className="whitespace-pre-wrap break-all text-base-content/85 py-1">
                      {item.message}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5" className="text-center py-8 text-base-content/40">
                    No log entries match your filter queries.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Actions */}
        {totalPages > 1 && (
          <div className="flex justify-between items-center pt-2 text-xs">
            <span className="text-base-content/50">
              Showing page <strong>{currentPage}</strong> of {totalPages} ({filteredTimeline.length} entries)
            </span>
            <div className="join">
              <button
                className="join-item btn btn-xs btn-outline"
                disabled={currentPage === 1}
                onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
              >
                Prev
              </button>
              <button
                className="join-item btn btn-xs btn-outline"
                disabled={currentPage === totalPages}
                onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
              >
                Next
              </button>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

export default LogTimelineInspector;
