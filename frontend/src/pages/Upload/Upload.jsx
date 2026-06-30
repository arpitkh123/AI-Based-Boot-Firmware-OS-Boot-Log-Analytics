import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useDropzone } from "react-dropzone";
import { UploadCloud, FileText, X, AlertCircle, CheckCircle2, Cpu, ShieldCheck, Terminal, Layers } from "lucide-react";
import { toast } from "react-toastify";
import PageTransition from "../../components/shared/PageTransition";

const ACCEPTED_EXTENSIONS = [".txt", ".log"];
const MAX_SIZE_MB = 50;

function validateFile(file) {
  const ext = "." + file.name.split(".").pop().toLowerCase();
  if (!ACCEPTED_EXTENSIONS.includes(ext)) {
    return `Invalid file type "${ext}". Only .txt and .log files are accepted.`;
  }
  if (file.size > MAX_SIZE_MB * 1024 * 1024) {
    return `File too large. Maximum is ${MAX_SIZE_MB}MB.`;
  }
  return null;
}

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

function UploadPage() {
  const navigate = useNavigate();

  const [selectedFile, setSelectedFile] = useState(null);
  const [fileError, setFileError] = useState(null);

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    setFileError(null);

    if (rejectedFiles.length > 0) {
      const msg = "Invalid file. Only .txt and .log files are accepted.";
      setFileError(msg);
      toast.error(msg);
      return;
    }

    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    const error = validateFile(file);

    if (error) {
      setFileError(error);
      toast.error(error);
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
    const shortName = file.name.length > 30 ? file.name.slice(0, 30) + "..." : file.name;
    toast.success(`"${shortName}" ready for analysis.`);
  }, []);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: { "text/plain": [".txt", ".log"] },
    maxFiles: 1,
    multiple: false,
  });

  const handleClearFile = () => {
    setSelectedFile(null);
    setFileError(null);
  };

  const handleAnalyze = () => {
    if (!selectedFile) return;
    navigate("/processing", { state: { file: selectedFile } });
  };

  const dropZoneClasses = [
    "border-2 border-dashed rounded-xl p-14 cursor-pointer",
    "transition-all duration-200 outline-none flex-1 flex flex-col items-center justify-center min-h-[280px]",
    isDragReject
      ? "border-error bg-error/10"
      : isDragActive
      ? "border-primary bg-primary/10"
      : "border-base-300 hover:border-primary bg-base-200/20 hover:bg-base-200/50",
  ].join(" ");

  return (
    <PageTransition>
      <div className="flex items-center justify-center p-4 lg:p-8">
        <div className="card w-full max-w-6xl bg-base-100 shadow-xl overflow-hidden">
          <div className="grid grid-cols-1 lg:grid-cols-12">
            
            {/* ── Left Column: Product Information & Tech Specs ── */}
            <div className="lg:col-span-5 bg-gradient-to-br from-neutral-900 to-neutral-950 text-neutral-100 p-8 lg:p-12 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-base-300">
              <div className="space-y-8">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-primary/10 rounded-lg text-primary">
                    <Cpu size={28} />
                  </div>
                  <div>
                    <span className="text-[10px] font-mono tracking-widest text-primary uppercase block font-semibold">
                      Enterprise Suite
                    </span>
                    <span className="text-lg font-bold tracking-tight">
                      HPE Boot Diagnostics
                    </span>
                  </div>
                </div>

                <div className="space-y-4">
                  <h1 className="text-3xl lg:text-4xl font-extrabold tracking-tight text-white leading-tight">
                    Boot Log Analytics
                  </h1>
                  <p className="text-neutral-400 text-sm leading-relaxed">
                    Identify firmware hang-ups, boot device timeouts, and kernel panic conditions with deep neural log profiling.
                  </p>
                </div>

                <div className="space-y-4 pt-4">
                  <div className="flex gap-3 items-start">
                    <div className="mt-1 p-1 bg-success/15 rounded text-success">
                      <ShieldCheck size={14} />
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-white">Isolation Forest Anomaly Detection</p>
                      <p className="text-[11px] text-neutral-400">Locates hardware register mismatches and sequence delays.</p>
                    </div>
                  </div>

                  <div className="flex gap-3 items-start">
                    <div className="mt-1 p-1 bg-primary/15 rounded text-primary">
                      <Terminal size={14} />
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-white">UART Log Template Parsing</p>
                      <p className="text-[11px] text-neutral-400">Normalizes dynamic timestamp segments and hex dumps instantly.</p>
                    </div>
                  </div>

                  <div className="flex gap-3 items-start">
                    <div className="mt-1 p-1 bg-secondary/15 rounded text-secondary">
                      <Layers size={14} />
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-white">Gemini AI Explanations</p>
                      <p className="text-[11px] text-neutral-400">Generates precise root cause summaries and suggested resolutions.</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="pt-8 lg:pt-0 border-t border-neutral-800 mt-8 lg:mt-0 flex justify-between items-center text-[10px] font-mono text-neutral-500">
                <span>SECURE END-TO-END DECRYPTED</span>
                <span>v1.0.0</span>
              </div>
            </div>

            {/* ── Right Column: File Drop & Actions ── */}
            <div className="lg:col-span-7 p-8 lg:p-12 flex flex-col justify-center gap-6">
              <div className="space-y-1">
                <h2 className="text-xl font-bold text-base-content">
                  Upload Logs
                </h2>
                <p className="text-xs text-base-content/50">
                  Select or drag a system boot console record to proceed.
                </p>
              </div>

              {/* ── Drop Zone ── */}
              <div {...getRootProps({ className: dropZoneClasses })}>
                <input {...getInputProps()} id="log-file-input" />
                <div className="flex flex-col items-center gap-4 pointer-events-none select-none text-center">
                  {isDragReject ? (
                    <AlertCircle size={48} className="text-error" />
                  ) : (
                    <UploadCloud
                      size={48}
                      className={isDragActive ? "text-primary" : "text-base-content/30"}
                    />
                  )}

                  <div className="space-y-1">
                    <p className="font-semibold text-base-content text-sm">
                      {isDragReject
                        ? "File type not supported"
                        : isDragActive
                        ? "Release to upload"
                        : "Drag & drop your boot log here"}
                    </p>
                    <p className="text-xs text-base-content/40">
                      {isDragActive ? "" : "or click to browse files"}
                    </p>
                  </div>

                  <div className="flex gap-2">
                    <span className="badge badge-neutral font-mono text-[10px]">.txt</span>
                    <span className="badge badge-neutral font-mono text-[10px]">.log</span>
                    <span className="badge badge-neutral font-mono text-[10px]">Max {MAX_SIZE_MB}MB</span>
                  </div>
                </div>
              </div>

              {/* ── Validation Error ── */}
              {fileError && (
                <div className="alert alert-error py-3 rounded-lg overflow-hidden flex items-center">
                  <AlertCircle size={16} className="shrink-0" />
                  <span className="text-xs font-semibold truncate break-all">{fileError}</span>
                </div>
              )}

              {/* ── Selected File Info with Overflow Fix ── */}
              {selectedFile && !fileError && (
                <div className="alert alert-success py-3 rounded-lg overflow-hidden flex justify-between items-center">
                  <div className="flex items-center gap-3 min-w-0 flex-1">
                    <CheckCircle2 size={16} className="text-success shrink-0" />
                    <div className="min-w-0 flex-1">
                      <p className="font-bold text-xs truncate text-base-content" title={selectedFile.name}>
                        {selectedFile.name}
                      </p>
                      <p className="text-[10px] text-base-content/60 font-mono">
                        {formatSize(selectedFile.size)}
                      </p>
                    </div>
                  </div>
                  <button
                    type="button"
                    id="clear-file-btn"
                    className="btn btn-ghost btn-xs shrink-0 rounded-lg hover:bg-success/20 ml-2"
                    onClick={handleClearFile}
                    title="Remove file"
                  >
                    <X size={14} />
                  </button>
                </div>
              )}

              {/* ── Analyze Button ── */}
              <button
                id="analyze-btn"
                className="btn btn-primary w-full gap-2 text-sm font-bold uppercase tracking-wider"
                disabled={!selectedFile || !!fileError}
                onClick={handleAnalyze}
              >
                <UploadCloud size={16} />
                Analyze Boot Log
              </button>
            </div>

          </div>
        </div>
      </div>
    </PageTransition>
  );
}

export default UploadPage;