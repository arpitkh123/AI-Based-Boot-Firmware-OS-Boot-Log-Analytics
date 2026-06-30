/**
 * PROCESSING_STEPS defines the ordered pipeline stages shown on the
 * Processing screen. Each string maps to one animation step (500ms each).
 * Keep this in sync with the actual backend pipeline for accuracy.
 */
export const PROCESSING_STEPS = [
  "Reading Boot Log",
  "Parsing UART Logs",
  "Extracting Templates",
  "Feature Engineering",
  "Running ML Model",
  "Rule-Based Analysis",
  "Generating AI Recommendation",
];
