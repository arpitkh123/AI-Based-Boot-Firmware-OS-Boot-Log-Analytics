import { useState } from "react";
import { Sliders, Cpu, Save, RefreshCw, Database } from "lucide-react";
import { toast } from "react-toastify";
import PageTransition from "../../components/shared/PageTransition";

function Settings() {
  const [modelType, setModelType] = useState("isolation_forest");
  const [confidenceThreshold, setConfidenceThreshold] = useState(80);
  const [enableGemini, setEnableGemini] = useState(true);
  const [saving, setSaving] = useState(false);

  const handleSave = () => {
    setSaving(true);
    setTimeout(() => {
      setSaving(false);
      toast.success("Diagnostic configuration saved successfully!");
    }, 800);
  };

  return (
    <PageTransition>
      <div className="max-w-4xl mx-auto space-y-6">
        
        {/* ── Page Header ── */}
        <div>
          <h1 className="text-2xl font-extrabold tracking-tight text-base-content">
            System Settings
          </h1>
          <p className="text-xs text-base-content/50 mt-1">
            Configure machine learning classifiers, neural templates, and analysis threshold limits.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* ── Left Sidebar Navigation Placeholder ── */}
          <div className="md:col-span-1 space-y-2">
            <button className="btn btn-ghost btn-sm justify-start w-full text-left bg-base-100 border border-base-300 font-bold text-primary">
              <Sliders size={16} className="mr-2" />
              Classifier Config
            </button>
            <button className="btn btn-ghost btn-sm justify-start w-full text-left text-base-content/60" disabled>
              <Database size={16} className="mr-2" />
              Database Storage
            </button>
          </div>

          {/* ── Settings Form ── */}
          <div className="md:col-span-2 card bg-base-100 shadow-xl border border-base-300 overflow-hidden">
            <div className="card-body gap-6 p-6 lg:p-8">
              
              <div className="flex items-center gap-2 pb-2 border-b border-base-300">
                <Cpu size={18} className="text-primary" />
                <h2 className="font-bold text-sm uppercase tracking-wider text-base-content/75 font-mono">
                  Machine Learning Model Settings
                </h2>
              </div>

              {/* Setting Row 1: Model Choice */}
              <div className="w-full space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-bold text-base-content/85">Core Classifier Model</span>
                  <span className="badge badge-primary font-mono text-[9px] px-2 py-0.5">ACTIVE</span>
                </div>
                <select 
                  className="select select-bordered select-sm w-full rounded-lg text-sm bg-base-200/40"
                  value={modelType}
                  onChange={(e) => setModelType(e.target.value)}
                >
                  <option value="isolation_forest">Isolation Forest Anomaly Classifier (Production)</option>
                  <option value="random_forest" disabled>Random Forest Template Matcher (Experimental)</option>
                  <option value="rule_based" disabled>Fallback Standard Ruleset (Legacy)</option>
                </select>
                <p className="text-[11px] text-base-content/40 leading-relaxed">
                  Selects the active AI pipeline engine for detecting out-of-order UART execution sequences.
                </p>
              </div>

              {/* Setting Row 2: Confidence Threshold */}
              <div className="w-full space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-bold text-base-content/85">Confidence Alarm Limit</span>
                  <span className="badge badge-primary font-mono text-xs font-semibold">{confidenceThreshold}%</span>
                </div>
                <input 
                  type="range" 
                  min="50" 
                  max="100" 
                  value={confidenceThreshold} 
                  className="range range-primary range-xs w-full cursor-pointer" 
                  onChange={(e) => setConfidenceThreshold(Number(e.target.value))}
                />
                <p className="text-[11px] text-base-content/40 leading-relaxed">
                  Logs classified with probability parameters below this threshold flag warnings instead of standard error alerts.
                </p>
              </div>

              {/* Setting Row 3: Gemini AI Explanation Toggle */}
              <div className="w-full p-4 bg-base-200/50 rounded-xl border border-base-300 flex items-center justify-between gap-4">
                <div className="space-y-1 min-w-0 flex-1">
                  <span className="text-sm font-bold text-base-content block">Gemini AI Log Interpretation</span>
                  <p className="text-[11px] text-base-content/50 leading-relaxed">
                    When enabled, diagnostic templates are routed securely to Gemini 1.5 to output human-readable remediation cards.
                  </p>
                </div>
                <input 
                  type="checkbox" 
                  className="toggle toggle-primary toggle-sm shrink-0 cursor-pointer" 
                  checked={enableGemini}
                  onChange={(e) => setEnableGemini(e.target.checked)}
                />
              </div>

              {/* Actions Footer */}
              <div className="flex justify-end gap-3 pt-4 border-t border-base-300">
                <button 
                  className="btn btn-primary btn-sm min-w-[120px] font-bold uppercase tracking-wider text-xs"
                  onClick={handleSave}
                  disabled={saving}
                >
                  {saving ? (
                    <>
                      <RefreshCw size={14} className="animate-spin mr-1" />
                      Saving
                    </>
                  ) : (
                    <>
                      <Save size={14} className="mr-1" />
                      Save Settings
                    </>
                  )}
                </button>
              </div>

            </div>
          </div>

        </div>

      </div>
    </PageTransition>
  );
}

export default Settings;