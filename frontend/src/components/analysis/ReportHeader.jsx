function ReportHeader({ analysisId, processing }) {

  const today = new Date().toLocaleString();

  return (
    <div className="navbar bg-base-100 rounded-xl shadow mb-6 px-6">

      <div className="flex-1">

        <div>

          <h1 className="text-3xl font-bold">
            AI Boot Firmware & OS Boot Analytics
          </h1>

          <p className="text-sm opacity-70">
            Analysis Report
          </p>

        </div>

      </div>

      <div className="text-right text-sm">

        <p>
          <strong>ID:</strong> {analysisId}
        </p>

        <p>
          <strong>Time:</strong> {processing.time}s
        </p>

        <p>
          {today}
        </p>

      </div>

    </div>
  );
}

export default ReportHeader;






// function ReportHeader({ analysisId, processing }) {
//   return (
//     <div className="bg-base-100 rounded-xl shadow p-6 mb-6">
//       <div className="flex justify-between items-center">

//         <div>
//           <h1 className="text-3xl font-bold">
//             AI Boot Log Analysis Report
//           </h1>

//           <p className="text-sm opacity-70 mt-1">
//             Generated Diagnostic Report
//           </p>
//         </div>

//         <div className="text-right">
//           <p>
//             <span className="font-semibold">Analysis ID:</span>
//             {" "}
//             {analysisId}
//           </p>

//           <p>
//             <span className="font-semibold">
//               Processing Time:
//             </span>
//             {" "}
//             {processing.time}s
//           </p>
//         </div>

//       </div>
//     </div>
//   );
// }

// export default ReportHeader;