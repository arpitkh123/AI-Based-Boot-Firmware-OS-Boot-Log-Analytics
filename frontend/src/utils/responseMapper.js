export function mapAnalysisResponse(response) {
  // Ensure default structures are safe if missing
  const defaultBootProgress = {
    kernelStarted: false,
    rootfsMounted: false,
    initStarted: false,
    loginPromptDetected: false,
    bootSuccessful: false
  };

  const defaultFailures = {
    kernelPanic: false,
    irqFailure: false,
    dmaFailure: false,
    rootfsFailure: false,
    dtbFailure: false,
    oomDetected: false,
    cpuFailure: false,
    filesystemFailure: false,
    initFailure: false
  };

  const bootData = response.boot || {};

  return {
    analysisId: response.analysisId,
    metadata: response.metadata || {},
    prediction: response.prediction || {},

    boot: {
      bootSuccessful: bootData.bootSuccessful !== undefined ? bootData.bootSuccessful : true,
      bootDuration: bootData.bootDuration !== undefined ? bootData.bootDuration : 5.0,
      bootStage: bootData.bootStage || "BOOT_SUCCESS",
      failureStage: bootData.failureStage || "N/A",
      failureType: bootData.failureType || null,
      failureReason: bootData.failureReason || null,
      failureLog: bootData.failureLog || null,
      bootProgress: bootData.bootProgress || defaultBootProgress,
      failures: bootData.failures || defaultFailures
    },

    statistics: response.statistics,
    recommendation: response.recommendation || { technicalReport: "" },
    processing: response.processing,

    details: response.details || {
      filename: "boot.log",
      fileSizeBytes: 0,
      bootSource: "Raw UART",
      startTimestamp: 0.0,
      endTimestamp: 0.0,
      lastMessage: "N/A",
      machineModel: "Unknown Hardware",
      linuxVersion: "N/A"
    },

    timeline: response.timeline || [],

    severitySummary: response.severitySummary || {
      "INFO": 0,
      "SUCCESS": 0,
      "WARNING": 0,
      "ERROR": 0
    },

    subsystemSummary: response.subsystemSummary || {
      "BOOT": 0,
      "KERNEL": 0,
      "MEMORY": 0,
      "FILESYSTEM": 0,
      "USB": 0,
      "NETWORK": 0,
      "UART": 0,
      "UNKNOWN": 0
    }
  };
}