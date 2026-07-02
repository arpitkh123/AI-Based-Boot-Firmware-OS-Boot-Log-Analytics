import {
  AlertTriangle,
  Info,
  Wrench,
  Brain,
  ChevronDown,
  ChevronUp
} from "lucide-react";
import { Marked } from "marked";
import { useEffect, useState } from "react";

// Instantiating marked parser
const marked = new Marked();

/**
 * Parses markdown to extract sections dynamically based on standard numbered headers (e.g. "1.", "2.")
 * or custom string titles. Returns an array of parsed segments.
 */
function parseGeminiMarkdownSections(text) {
  if (!text) return [];

  // Split by line to identify section headers
  const lines = text.split("\n");
  const sections = [];
  let currentSection = null;

  for (let line of lines) {
    const trimmed = line.trim();
    
    // Detect standard section headers matching: Number. Title (e.g., "1. Overall Boot Status" or "2. Boot Stage")
    const headerMatch = trimmed.match(/^(\d+)\.\s*(.+)$/);
    
    if (headerMatch) {
      if (currentSection) {
        sections.push(currentSection);
      }
      currentSection = {
        id: headerMatch[1],
        title: headerMatch[2].replace(/\*\*/g, ""), // strip out markdown bold markers if nested
        contentLines: []
      };
    } else if (currentSection) {
      currentSection.contentLines.push(line);
    } else {
      // Fallback for lines before the first numbered section header
      if (trimmed.length > 0) {
        if (!sections.some(s => s.id === "intro")) {
          sections.push({
            id: "intro",
            title: "Analysis Briefing",
            contentLines: [line]
          });
        } else {
          sections[0].contentLines.push(line);
        }
      }
    }
  }

  if (currentSection) {
    sections.push(currentSection);
  }

  // Convert content lines back to raw string block
  return sections.map(s => ({
    ...s,
    content: s.contentLines.join("\n").trim()
  })).filter(s => s.content.length > 0 || s.title.length > 0);
}

function SectionCollapseCard({ id, title, content }) {
  const [open, setOpen] = useState(id === "1" || id === "intro"); // Keep first/intro open by default
  const [htmlContent, setHtmlContent] = useState("");

  useEffect(() => {
    if (content) {
      setHtmlContent(marked.parse(content));
    }
  }, [content]);

  return (
    <div className="border border-base-300 rounded-xl bg-base-200/50 overflow-hidden transition-all duration-200">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex justify-between items-center p-4 font-mono font-bold text-xs uppercase tracking-wider bg-base-300/40 hover:bg-base-300/80 transition-colors text-left"
      >
        <div className="flex items-center gap-3">
          <span className="badge badge-primary badge-sm font-semibold">{id}</span>
          <span className="text-base-content/90 font-semibold">{title}</span>
        </div>
        {open ? <ChevronUp size={16} className="opacity-70" /> : <ChevronDown size={16} className="opacity-70" />}
      </button>
      
      {open && (
        <div className="p-5 border-t border-base-300/70 bg-base-100/30">
          <div 
            className="text-sm text-base-content leading-relaxed markdown-body prose prose-sm max-w-none text-justify"
            dangerouslySetInnerHTML={{ __html: htmlContent }}
          />
        </div>
      )}
    </div>
  );
}

function RecommendationCard({ recommendation, bootStatus }) {
  // Use technicalReport directly as the source of truth
  const reportText = recommendation.technicalReport || recommendation.reason || "";
  const parsedSections = parseGeminiMarkdownSections(reportText);

  const rootCauseAccent = bootStatus
    ? "border-info"
    : "border-error";

  const rootCauseIcon = bootStatus ? Info : AlertTriangle;

  return (
    <div className="card bg-base-100 shadow mb-6 border border-base-300">
      <div className="card-body gap-5">

        {/* Header */}
        <div className="flex items-center gap-2 border-b border-base-300 pb-3">
          <Brain size={18} className="text-primary" />
          <h2 className="card-title text-base font-bold">
            AI Technical Explanation &amp; Diagnostics
          </h2>
        </div>

        {/* Root Cause — alert style banner */}
        {recommendation.rootCause && (
          <div className={`flex gap-4 p-4 rounded-xl border-l-4 bg-base-200/60 ${rootCauseAccent}`}>
            <div className="shrink-0 mt-0.5">
              {bootStatus ? <Info size={18} className="text-info" /> : <AlertTriangle size={18} className="text-error" />}
            </div>
            <div className="space-y-1">
              <span className="text-xs font-mono uppercase tracking-widest text-base-content/40 block">Classification Summary</span>
              <p className="text-sm font-bold text-base-content leading-relaxed">
                {recommendation.rootCause}
              </p>
            </div>
          </div>
        )}

        {/* Suggested Resolution */}
        {recommendation.solution && (
          <div className="flex gap-4 p-4 rounded-xl border-l-4 bg-base-200/60 border-success">
            <Wrench size={18} className="shrink-0 mt-0.5 text-success" />
            <div className="space-y-1">
              <span className="text-xs font-mono uppercase tracking-widest text-base-content/40 block">Immediate Actions Needed</span>
              <p className="text-sm text-base-content font-medium leading-relaxed">
                {recommendation.solution}
              </p>
            </div>
          </div>
        )}

        {/* Dynamic Section Breakdowns from Gemini Analysis Report */}
        <div className="space-y-3">
          <div className="text-xs font-mono uppercase tracking-widest text-base-content/40 mb-1 pl-1">
            Deep-Dive Diagnostic Report
          </div>
          {parsedSections.length > 0 ? (
            parsedSections.map((sec) => (
              <SectionCollapseCard
                key={sec.id}
                id={sec.id}
                title={sec.title}
                content={sec.content}
              />
            ))
          ) : (
            <div className="text-xs text-base-content/40 p-4 bg-base-200/20 rounded-xl text-center font-mono">
              Detailed log interpretation report segment is empty.
            </div>
          )}
        </div>

      </div>
    </div>
  );
}

export default RecommendationCard;