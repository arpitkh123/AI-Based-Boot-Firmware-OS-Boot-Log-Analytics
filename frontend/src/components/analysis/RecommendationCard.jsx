import {
  AlertTriangle,
  Info,
  Wrench,
  Brain,
} from "lucide-react";
import { Marked } from "marked";
import { useEffect, useState } from "react";

// Instantiating marked parser
const marked = new Marked();

/**
 * A single section within the AI explanation panel.
 * accent controls the left-border color and icon color.
 * Uses marked to parse markdown content safely.
 */
function ExplanationSection({ icon: Icon, label, accentClass, text }) {
  const [htmlContent, setHtmlContent] = useState("");

  useEffect(() => {
    if (text) {
      // Parse markdown to HTML
      const rawHtml = marked.parse(text);
      setHtmlContent(rawHtml);
    }
  }, [text]);

  return (
    <div className={`flex gap-4 p-4 rounded-lg border-l-4 bg-base-200 ${accentClass}`}>
      <Icon size={18} className="shrink-0 mt-1 opacity-70" />
      <div className="space-y-1 min-w-0 flex-1">
        <p className="text-xs font-mono uppercase tracking-widest text-base-content/40 mb-2">
          {label}
        </p>
        <div 
          className="text-sm text-base-content leading-relaxed markdown-body prose prose-sm max-w-none text-justify"
          dangerouslySetInnerHTML={{ __html: htmlContent }}
        />
      </div>
    </div>
  );
}

function RecommendationCard({ recommendation, bootStatus }) {
  const rootCauseAccent = bootStatus
    ? "border-info"
    : "border-error";

  const rootCauseIcon = bootStatus ? Info : AlertTriangle;

  return (
    <div className="card bg-base-100 shadow mb-6">
      <div className="card-body gap-4">

        {/* Header */}
        <div className="flex items-center gap-2 mb-1">
          <Brain size={18} className="text-primary" />
          <h2 className="card-title text-base">
            AI Technical Explanation
          </h2>
        </div>

        {/* Root Cause — color depends on boot outcome */}
        <ExplanationSection
          icon={rootCauseIcon}
          label="Root Cause"
          accentClass={rootCauseAccent}
          text={recommendation.rootCause}
        />

        {/* Reason — always neutral/informational */}
        <ExplanationSection
          icon={Info}
          label="Analysis"
          accentClass="border-warning"
          text={recommendation.reason}
        />

        {/* Solution — always positive/actionable */}
        <ExplanationSection
          icon={Wrench}
          label="Suggested Resolution"
          accentClass="border-success"
          text={recommendation.solution}
        />

      </div>
    </div>
  );
}

export default RecommendationCard;