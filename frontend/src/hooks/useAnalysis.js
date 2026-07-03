import { useEffect, useState, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

import { analyzeLog } from "../services/analysisService";
import { PROCESSING_STEPS } from "../constants/steps";

/**
 * useAnalysis
 *
 * Manages the full analysis lifecycle for the Processing page:
 *  - Guards against missing file state (redirects to /upload)
 *  - Calls the backend API concurrently with the step animation
 *  - Advances the current step every 500ms
 *  - Waits for the backend to finish before navigating to /analysis
 *  - Replaces alert() with toast.error() for error feedback
 *  - Cleans up intervals and prevents state updates after unmount
 *  - Ensures API is only called once even under React 18/19 StrictMode double mount.
 *
 * @returns {{ currentStep: number, totalSteps: number }}
 */
export function useAnalysis() {
  const navigate = useNavigate();
  const location = useLocation();

  const file = location.state?.file;
  const apiCalled = useRef(false);

  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    if (!file) {
      navigate("/upload");
      return;
    }

    let backendResult = null;
    let backendFinished = false;
    let cancelled = false;
    let stepInterval = null;
    let waitInterval = null;

    const callBackend = async () => {
      if (apiCalled.current) return;
      apiCalled.current = true;
      try {
        backendResult = await analyzeLog(file);
        backendFinished = true;
      } catch (error) {
        console.error("[useAnalysis] Backend error:", error);

        if (!cancelled) {
          toast.error(
            "Analysis failed. Please verify the file format and try again.",
            { autoClose: 6000 }
          );
          navigate("/upload");
        }
      }
    };

    callBackend();

    let step = 0;

    stepInterval = setInterval(() => {
      if (cancelled) return;

      step++;
      setCurrentStep(step);

      if (step >= PROCESSING_STEPS.length) {
        clearInterval(stepInterval);

        // Poll until backend finishes, then navigate
        waitInterval = setInterval(() => {
          if (cancelled) {
            clearInterval(waitInterval);
            return;
          }

          if (backendFinished) {
            clearInterval(waitInterval);
            navigate("/analysis", {
              state: { result: backendResult },
            });
          }
        }, 200);
      }
    }, 500);

    // Cleanup: clear all intervals and mark as cancelled on unmount
    return () => {
      cancelled = true;
      clearInterval(stepInterval);
      clearInterval(waitInterval);
    };
  }, [file, navigate]);

  return {
    currentStep,
    totalSteps: PROCESSING_STEPS.length,
  };
}
