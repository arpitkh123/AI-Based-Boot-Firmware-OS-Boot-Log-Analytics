import { useLocation, Link } from "react-router-dom";
import { AlertCircle, ArrowLeft } from "lucide-react";

import { mapAnalysisResponse } from "../../utils/responseMapper";
import PageTransition from "../../components/shared/PageTransition";

import ReportHeader from "../../components/analysis/ReportHeader";
import PredictionCard from "../../components/analysis/PredictionCard";
import BootSummaryCard from "../../components/analysis/BootSummaryCard";
import ProcessingInfoCard from "../../components/analysis/ProcessingInfoCard";
import StatisticsCard from "../../components/analysis/StatisticsCard";
import SubsystemDistribution from "../../components/analysis/SubsystemDistribution";
import BootParserConsole from "../../components/analysis/BootParserConsole";
import RecommendationCard from "../../components/analysis/RecommendationCard";
import LogTimelineInspector from "../../components/analysis/LogTimelineInspector";
import ReportActions from "../../components/analysis/ReportActions";

function Analysis() {
  const location = useLocation();

  const response = location.state?.result;

  if (!response) {
    return (
      <PageTransition>
        <div className="max-w-md mx-auto my-16 text-center space-y-6 p-8 card bg-base-100 shadow-xl border border-base-300">
          <AlertCircle size={48} className="mx-auto text-warning animate-pulse" />
          <div className="space-y-2">
            <h2 className="text-xl font-bold text-base-content">No Active Analysis Report</h2>
            <p className="text-xs text-base-content/60 leading-relaxed">
              You haven't run or selected any logs for diagnosis. Please upload a log file or browse your diagnostic history.
            </p>
          </div>
          <div className="flex flex-col sm:flex-row gap-3 justify-center pt-2">
            <Link to="/upload" className="btn btn-primary btn-sm rounded-lg flex items-center gap-2">
              <ArrowLeft size={14} /> Upload a Log
            </Link>
            <Link to="/history" className="btn btn-outline btn-sm rounded-lg">
              View History
            </Link>
          </div>
        </div>
      </PageTransition>
    );
  }

  const analysis = mapAnalysisResponse(response);

  return (
    <PageTransition>
      <div className="min-h-screen bg-base-200 p-8">
        <div className="max-w-7xl mx-auto">
          <ReportHeader
            analysisId={analysis.analysisId}
            file={{
              name: analysis.details?.filename,
              sizeBytes: analysis.details?.fileSizeBytes,
              uploadedAt: analysis.metadata?.timestamp || new Date().toISOString()
            }}
            processing={analysis.processing}
            prediction={{
              severity: analysis.prediction?.severity || "INFO"
            }}
            environment={{
              machineModel: analysis.details?.machineModel,
              linuxVersion: analysis.details?.linuxVersion,
              bootType: analysis.details?.bootSource
            }}
          />

          <PredictionCard
            prediction={analysis.prediction}
            bootStatus={analysis.boot.bootSuccessful}
          />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <BootSummaryCard boot={analysis.boot} details={analysis.details} />
            <ProcessingInfoCard
              processing={analysis.processing}
              statistics={analysis.statistics}
              analysisId={analysis.analysisId}
              details={analysis.details}
            />
          </div>

          <StatisticsCard statistics={analysis.statistics} />

          <BootParserConsole boot={analysis.boot} />

          <SubsystemDistribution
            severitySummary={analysis.severitySummary}
            subsystemSummary={analysis.subsystemSummary}
          />

          <RecommendationCard
            recommendation={analysis.recommendation}
            bootStatus={analysis.boot.bootSuccessful}
          />

          <LogTimelineInspector timeline={analysis.timeline} />

          <ReportActions analysis={analysis} />
        </div>
      </div>
    </PageTransition>
  );
}

export default Analysis;