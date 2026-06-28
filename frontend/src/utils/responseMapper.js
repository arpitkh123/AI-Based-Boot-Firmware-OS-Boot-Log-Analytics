export function mapAnalysisResponse(response) {
  return {
    analysisId: response.analysisId,

    prediction: response.prediction,

    boot: response.boot,

    statistics: response.statistics,

    recommendation: response.recommendation,

    processing: response.processing,
  };
}