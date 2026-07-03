import { useNavigate } from "react-router-dom";
import { UploadCloud, Download, FileJson } from "lucide-react";

/**
 * Triggers a browser download of data as a formatted JSON file.
 */
function downloadJson(data, filename) {
  const blob = new Blob(
    [JSON.stringify(data, null, 2)],
    { type: "application/json" }
  );
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  document.body.removeChild(anchor);
  URL.revokeObjectURL(url);
}

function ReportActions({ analysis }) {
  const navigate = useNavigate();

  const handleNewAnalysis = () => {
    navigate("/upload");
  };

  const handleDownloadJson = () => {
    const filename = `boot-analysis-${analysis?.analysisId ?? "report"}.json`;
    downloadJson(analysis, filename);
  };

  const handlePrintPdf = () => {
    window.print();
  };

  return (
    <div className="flex flex-wrap justify-end items-center gap-3 py-6 border-t border-base-300 mt-2 no-print">

      {/* New Analysis — navigates back to upload */}
      <button
        id="new-analysis-btn"
        className="btn btn-outline btn-sm gap-2"
        onClick={handleNewAnalysis}
      >
        <UploadCloud size={15} />
        New Analysis
      </button>

      {/* Download PDF — Native window print layout */}
      <button
        id="download-pdf-btn"
        className="btn btn-secondary btn-sm gap-2"
        onClick={handlePrintPdf}
        disabled={!analysis}
      >
        <Download size={15} />
        Print PDF Report
      </button>

      {/* Download JSON — fully functional */}
      <button
        id="download-json-btn"
        className="btn btn-primary btn-sm gap-2"
        onClick={handleDownloadJson}
        disabled={!analysis}
      >
        <FileJson size={15} />
        Download JSON
      </button>

    </div>
  );
}

export default ReportActions;