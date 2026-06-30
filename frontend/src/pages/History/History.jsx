import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Calendar, Clock, ChevronRight, FileText, CheckCircle2, XCircle, Search, Trash2, RefreshCw } from "lucide-react";
import PageTransition from "../../components/shared/PageTransition";
import { getHistory, deleteHistoryItem } from "../../services/analysisService";
import { toast } from "react-toastify";

function History() {
  const navigate = useNavigate();
  const [historyList, setHistoryList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  const loadHistoryData = async () => {
    setLoading(true);
    try {
      const data = await getHistory();
      setHistoryList(data);
    } catch (error) {
      console.error("Failed to fetch history:", error);
      toast.error("Could not load diagnosis history logs.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistoryData();
  }, []);

  const handleRowClick = (item) => {
    if (item.result) {
      navigate("/analysis", { state: { result: item.result } });
    } else {
      toast.warning("Analysis report details are not available for this record.");
    }
  };

  const handleDelete = async (e, id) => {
    e.stopPropagation();
    try {
      await deleteHistoryItem(id);
      setHistoryList(prev => prev.filter(item => item.analysisId !== id));
      toast.success("Analysis report deleted.");
    } catch (error) {
      console.error("Failed to delete item:", error);
      toast.error("Could not delete report.");
    }
  };

  const filteredHistory = historyList.filter(item => 
    item.fileName.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.analysisId.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.class.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <PageTransition>
      <div className="max-w-6xl mx-auto space-y-6">
        
        {/* ── Page Header ── */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-2xl font-extrabold tracking-tight text-base-content">
              Diagnostic History
            </h1>
            <p className="text-xs text-base-content/50 mt-1">
              Browse previously executed firmware and OS boot analyses.
            </p>
          </div>
          
          <div className="flex items-center gap-3 w-full md:w-auto">
            {/* Search bar */}
            <div className="relative w-full md:w-72">
              <Search className="absolute left-3 top-2.5 text-base-content/40" size={16} />
              <input
                type="text"
                placeholder="Search history..."
                className="input input-sm input-bordered pl-10 w-full rounded-lg"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            
            <button 
              onClick={loadHistoryData} 
              className="btn btn-sm btn-ghost border border-base-300"
              title="Refresh"
            >
              <RefreshCw size={14} className={loading ? "animate-spin" : ""} />
            </button>
          </div>
        </div>

        {/* ── Table / Grid View ── */}
        <div className="card bg-base-100 shadow-xl overflow-hidden border border-base-300">
          {loading ? (
            <div className="p-16 text-center space-y-3">
              <RefreshCw size={36} className="mx-auto text-primary animate-spin" />
              <p className="text-xs text-base-content/50">Fetching logs from server...</p>
            </div>
          ) : filteredHistory.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="table w-full table-zebra">
                <thead>
                  <tr className="border-b border-base-300 bg-base-200/50">
                    <th className="font-mono text-xs uppercase tracking-wider text-base-content/55">Analysis ID</th>
                    <th className="font-mono text-xs uppercase tracking-wider text-base-content/55">File Name</th>
                    <th className="font-mono text-xs uppercase tracking-wider text-base-content/55">Status</th>
                    <th className="font-mono text-xs uppercase tracking-wider text-base-content/55">ML Classification</th>
                    <th className="font-mono text-xs uppercase tracking-wider text-base-content/55">Date Analyzed</th>
                    <th className="font-mono text-xs uppercase tracking-wider text-base-content/55 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredHistory.map((item) => (
                    <tr 
                      key={item.analysisId}
                      className="hover:bg-base-200/40 transition-colors duration-150 cursor-pointer"
                      onClick={() => handleRowClick(item)}
                    >
                      <td className="font-mono text-xs font-bold text-primary">{item.analysisId}</td>
                      <td className="max-w-[200px] truncate font-medium text-sm text-base-content" title={item.fileName}>
                        <div className="flex items-center gap-2">
                          <FileText size={14} className="text-base-content/40 shrink-0" />
                          <span className="truncate">{item.fileName}</span>
                        </div>
                      </td>
                      <td>
                        <span className={`badge badge-sm font-semibold gap-1.5 ${
                          item.status === "Successful" 
                            ? "badge-success bg-success/10 text-success border-success/20" 
                            : "badge-error bg-error/10 text-error border-error/20"
                        }`}>
                          {item.status === "Successful" ? <CheckCircle2 size={10} /> : <XCircle size={10} />}
                          {item.status}
                        </span>
                      </td>
                      <td className="text-xs font-semibold text-base-content/80 max-w-[200px] truncate" title={item.class}>
                        {item.class}
                      </td>
                      <td className="text-xs font-mono text-base-content/60">
                        {item.timestamp}
                      </td>
                      <td className="text-right">
                        <div className="flex justify-end items-center gap-2">
                          <button
                            onClick={(e) => handleDelete(e, item.analysisId)}
                            className="btn btn-ghost btn-xs text-error hover:bg-error/15 rounded-lg"
                            title="Delete Log"
                          >
                            <Trash2 size={13} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="p-16 text-center space-y-3">
              <FileText size={48} className="mx-auto text-base-content/20" />
              <div className="space-y-1">
                <p className="font-bold text-base-content text-sm">No analysis reports found</p>
                <p className="text-xs text-base-content/40 max-w-xs mx-auto">
                  Try adjusting your search queries or upload a new firmware log for processing.
                </p>
              </div>
            </div>
          )}
        </div>

      </div>
    </PageTransition>
  );
}

export default History;