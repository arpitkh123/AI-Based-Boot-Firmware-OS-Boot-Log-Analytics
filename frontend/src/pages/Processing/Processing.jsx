import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  CheckCircle2,
  Circle,
  LoaderCircle,
} from "lucide-react";

import { analyzeLog } from "../../services/analysisService";

const STEPS = [
  "Reading Boot Log",
  "Parsing UART Logs",
  "Extracting Templates",
  "Feature Engineering",
  "Running ML Model",
  "Rule-Based Analysis",
  "Generating AI Recommendation",
];

function Processing() {
  const navigate = useNavigate();
  const location = useLocation();

  const file = location.state?.file;

  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    if (!file) {
      navigate("/upload");
      return;
    }

    let backendResult = null;
    let backendFinished = false;

    const callBackend = async () => {
      try {
        backendResult = await analyzeLog(file);
        backendFinished = true;
      } catch (error) {
        console.error(error);
        alert("Analysis Failed");
        navigate("/upload");
      }
    };

    callBackend();

    let step = 0;

    const interval = setInterval(() => {
      step++;

      setCurrentStep(step);

      if (step >= STEPS.length) {
        clearInterval(interval);

        const waitForBackend = setInterval(() => {
          if (backendFinished) {
            clearInterval(waitForBackend);

            navigate("/analysis", {
              state: {
                result: backendResult,
              },
            });
          }
        }, 200);
      }
    }, 500);

    return () => clearInterval(interval);
  }, [file, navigate]);

  return (
    <div className="min-h-screen bg-base-200 flex items-center justify-center">

      <div className="card bg-base-100 shadow-xl w-full max-w-2xl">

        <div className="card-body">

          <h1 className="text-3xl font-bold text-center">
            AI Boot Log Analytics
          </h1>

          <p className="text-center opacity-70 mb-6">
            Processing Uploaded Boot Log...
          </p>

          <div className="space-y-4">

            {STEPS.map((step, index) => (
              <div
                key={step}
                className="flex items-center gap-3"
              >
                {index < currentStep ? (
                  <CheckCircle2 className="text-success" />
                ) : index === currentStep ? (
                  <LoaderCircle className="animate-spin text-primary" />
                ) : (
                  <Circle className="text-gray-400" />
                )}

                <span>{step}</span>
              </div>
            ))}

          </div>

          <div className="divider"></div>

          <p className="text-center text-sm opacity-60">
            Please wait while the AI analyzes the boot log...
          </p>

        </div>

      </div>

    </div>
  );
}

export default Processing;



// import { useEffect } from "react";
// import { useLocation, useNavigate } from "react-router-dom";

// import { analyzeLog } from "../../services/analysisService";

// function Processing() {
//   const navigate = useNavigate();
//   const location = useLocation();

//   const file = location.state?.file;

//   useEffect(() => {
//     const processLog = async () => {
//       if (!file) {
//         navigate("/upload");
//         return;
//       }

//       try {
//         console.log("Starting Analysis...");

//         const result = await analyzeLog(file);

//         console.log(result);

//         navigate("/analysis", {
//           state: {
//             result,
//           },
//         });
//       } catch (error) {
//         console.error(error);
//         alert("Failed to analyze log.");

//         navigate("/upload");
//       }
//     };

//     processLog();
//   }, [file, navigate]);

//   return (
//     <div style={{ padding: "40px" }}>
//       <h1>Analyzing Boot Log...</h1>

//       <p>Please wait while the system processes your file.</p>
//     </div>
//   );
// }

// export default Processing;




// function Processing() {
//     return <h1>Processing Page</h1>;
// }

// export default Processing;