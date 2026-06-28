import { useLocation, Navigate } from "react-router-dom";
// import PredictionCard from "../../components/analysis/PredictionCard";

import { mapAnalysisResponse } from "../../utils/responseMapper";
// import BootSummaryCard from "../../components/analysis/BootSummaryCard";
// import StatisticsCard from "../../components/analysis/StatisticsCard";
// import RecommendationCard from "../../components/analysis/RecommendationCard";

import ReportHeader from "../../components/analysis/ReportHeader";
import PredictionCard from "../../components/analysis/PredictionCard";
import BootSummaryCard from "../../components/analysis/BootSummaryCard";
import ProcessingInfoCard from "../../components/analysis/ProcessingInfoCard";
import StatisticsCard from "../../components/analysis/StatisticsCard";
import RecommendationCard from "../../components/analysis/RecommendationCard";
import ReportActions from "../../components/analysis/ReportActions";

function Analysis() {
  const location = useLocation();

  const response = location.state?.result;

//   const result = location.state?.result;

    if (!response) {
//   if (!result) {
        return <Navigate to="/upload" replace />;
    }

    const analysis = mapAnalysisResponse(response);



    return (
        <div className="min-h-screen bg-base-200 p-8">

            <div className="max-w-7xl mx-auto">

            <ReportHeader
                analysisId={analysis.analysisId}
                processing={analysis.processing}
            />

            <PredictionCard
                prediction={analysis.prediction}
                bootStatus={analysis.boot.bootSuccessful}
            />

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">

                <BootSummaryCard
                boot={analysis.boot}
                />

                <ProcessingInfoCard
                processing={analysis.processing}
                statistics={analysis.statistics}
                analysisId={analysis.analysisId}
                />

            </div>

            <StatisticsCard
                statistics={analysis.statistics}
            />

            <RecommendationCard
                recommendation={analysis.recommendation}
            />

            <ReportActions />

            </div>

        </div>
    );







    // return (
    //     <div style={{ padding: "40px" }}>
    //     <h1>Analysis Report</h1>

    //     <hr />

    //     <PredictionCard prediction={analysis.prediction} />
    //     <BootSummaryCard boot={analysis.boot} />
    //     <StatisticsCard statistics={analysis.statistics} />
    //     <RecommendationCard recommendation={analysis.recommendation} />

    //     {/* <pre>
    //         {JSON.stringify(result, null, 2)}
    //     </pre> */}
    //     </div>
    // );
}

export default Analysis;




// function Analysis() {
//     return <h1>Analysis Page</h1>;
// }

// export default Analysis;