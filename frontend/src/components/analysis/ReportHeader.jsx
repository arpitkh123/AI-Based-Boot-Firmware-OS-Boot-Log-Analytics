import {
  FileTerminal,
  CalendarDays,
  Clock3,
  HardDrive,
} from "lucide-react";

function formatDate(value) {
  if (!value) return "--";

  return new Date(value).toLocaleString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
}

function formatBytes(bytes) {
  if (!bytes) return "--";

  const units = ["B", "KB", "MB", "GB"];

  let size = bytes;
  let unit = 0;

  while (size >= 1024 && unit < units.length - 1) {
    size /= 1024;
    unit++;
  }

  return `${size.toFixed(1)} ${units[unit]}`;
}

function ReportHeader({
  analysisId,
  file,
  processing,
  prediction,
  environment,
}) {
  return (
    <div className="card bg-base-100 shadow mb-6">
      <div className="card-body">

        <div className="flex flex-col lg:flex-row justify-between gap-6">

          {/* Left */}

          <div>

            <div className="flex items-center gap-3">

              <FileTerminal
                size={24}
                className="text-primary"
              />

              <div>

                <h1 className="text-2xl font-bold">
                  Firmware Boot Analysis Report
                </h1>

                <p className="text-sm opacity-60">
                  AI Powered Boot Diagnostics
                </p>

              </div>

            </div>

            <div className="divider my-4"></div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">

              <div>

                <div className="font-semibold">
                  Uploaded File
                </div>

                <div className="opacity-70 break-all">
                  {file?.name ?? "--"}
                </div>

              </div>

              <div>

                <div className="font-semibold">
                  Machine
                </div>

                <div className="opacity-70">
                  {environment?.machineModel ?? "--"}
                </div>

              </div>

              <div>

                <div className="font-semibold">
                  Linux Version
                </div>

                <div className="opacity-70">
                  {environment?.linuxVersion ?? "--"}
                </div>

              </div>

              <div>

                <div className="font-semibold">
                  Boot Type
                </div>

                <div className="opacity-70">
                  {environment?.bootType ?? "--"}
                </div>

              </div>

            </div>

          </div>

          {/* Right */}

          <div className="grid grid-cols-2 gap-4 min-w-[320px]">

            <div className="stat bg-base-200 rounded-xl">

              <div className="stat-title">
                Analysis ID
              </div>

              <div className="stat-value text-base font-mono break-all">
                {analysisId}
              </div>

            </div>

            <div className="stat bg-base-200 rounded-xl">

              <div className="stat-title">
                Severity
              </div>

              <div className="stat-value text-lg">
                {prediction?.severity ?? "--"}
              </div>

            </div>

            <div className="stat bg-base-200 rounded-xl">

              <div className="stat-figure">
                <CalendarDays size={18} />
              </div>

              <div className="stat-title">
                Upload Time
              </div>

              <div className="text-sm">
                {formatDate(file?.uploadedAt)}
              </div>

            </div>

            <div className="stat bg-base-200 rounded-xl">

              <div className="stat-figure">
                <Clock3 size={18} />
              </div>

              <div className="stat-title">
                Processing
              </div>

              <div className="text-sm">
                {processing?.time ?? "--"} s
              </div>

            </div>

            <div className="stat bg-base-200 rounded-xl col-span-2">

              <div className="stat-figure">
                <HardDrive size={18} />
              </div>

              <div className="stat-title">
                File Size
              </div>

              <div className="text-sm">
                {formatBytes(file?.sizeBytes)}
              </div>

            </div>

          </div>

        </div>

      </div>
    </div>
  );
}

export default ReportHeader;





// import { FileTerminal } from "lucide-react";

// /**
//  * Formats a Date object to a consistent, locale-stable string.
//  * Example output: "30 Jun 2026, 01:10"
//  * Uses en-GB explicitly so the format never varies by user's system locale.
//  */
// function formatReportDate(date) {
//   return date.toLocaleString("en-GB", {
//     day: "2-digit",
//     month: "short",
//     year: "numeric",
//     hour: "2-digit",
//     minute: "2-digit",
//     hour12: false,
//   });
// }

// function ReportHeader({ analysisId, processing }) {
//   const generatedAt = formatReportDate(new Date());

//   return (
//     <div className="card bg-base-100 shadow mb-6">
//       <div className="card-body py-4">

//         <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">

//           {/* ── Left: title block ── */}
//           <div className="flex items-center gap-3">
//             <FileTerminal size={22} className="text-primary shrink-0" />
//             <div>
//               <h1 className="text-xl font-bold text-base-content leading-tight">
//                 AI Boot Firmware &amp; OS Boot Analytics
//               </h1>
//               <p className="text-xs text-base-content/40 mt-0.5">
//                 Analysis Report · Generated {generatedAt}
//               </p>
//             </div>
//           </div>

//           {/* ── Right: metadata strip ── */}
//           <div className="flex flex-wrap gap-x-6 gap-y-1 text-xs sm:text-right shrink-0">

//             <div>
//               <span className="text-base-content/40 uppercase tracking-wider font-mono">
//                 ID&nbsp;
//               </span>
//               <span className="font-mono text-base-content/70 break-all">
//                 {analysisId}
//               </span>
//             </div>

//             <div>
//               <span className="text-base-content/40 uppercase tracking-wider font-mono">
//                 Time&nbsp;
//               </span>
//               <span className="font-mono text-base-content/70">
//                 {processing.time}s
//               </span>
//             </div>

//           </div>

//         </div>

//       </div>
//     </div>
//   );
// }

// export default ReportHeader;