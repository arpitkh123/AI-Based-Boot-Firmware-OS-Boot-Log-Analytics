import {
  FileText,
  CircleX,
  TriangleAlert,
  Blocks,
  Brain,
} from "lucide-react";

function StatisticsCard({ statistics }) {
  return (
    <div className="stats shadow w-full mb-6">

      <div className="stat">

        <FileText size={22} />

        <div className="stat-value">
          {statistics.logsParsed}
        </div>

        <div className="stat-title">
          Logs
        </div>

      </div>

      <div className="stat">

        <CircleX
          className="text-error"
          size={22}
        />

        <div className="stat-value text-error">
          {statistics.errors}
        </div>

        <div className="stat-title">
          Errors
        </div>

      </div>

      <div className="stat">

        <TriangleAlert
          className="text-warning"
          size={22}
        />

        <div className="stat-value text-warning">
          {statistics.warnings}
        </div>

        <div className="stat-title">
          Warnings
        </div>

      </div>

      <div className="stat">

        <Blocks size={22} />

        <div className="stat-value">
          {statistics.templates}
        </div>

        <div className="stat-title">
          Templates
        </div>

      </div>

      <div className="stat">

        <Brain size={22} />

        <div className="stat-value">
          {statistics.features}
        </div>

        <div className="stat-title">
          Features
        </div>

      </div>

    </div>
  );
}

export default StatisticsCard;





// function StatisticsCard({ statistics }) {
//   return (
//     <div className="stats shadow w-full mb-6">

//       <div className="stat">
//         <div className="stat-value">
//           {statistics.logsParsed}
//         </div>
//         <div className="stat-title">
//           Logs
//         </div>
//       </div>

//       <div className="stat">
//         <div className="stat-value text-error">
//           {statistics.errors}
//         </div>
//         <div className="stat-title">
//           Errors
//         </div>
//       </div>

//       <div className="stat">
//         <div className="stat-value text-warning">
//           {statistics.warnings}
//         </div>
//         <div className="stat-title">
//           Warnings
//         </div>
//       </div>

//       <div className="stat">
//         <div className="stat-value">
//           {statistics.templates}
//         </div>
//         <div className="stat-title">
//           Templates
//         </div>
//       </div>

//       <div className="stat">
//         <div className="stat-value">
//           {statistics.features}
//         </div>
//         <div className="stat-title">
//           Features
//         </div>
//       </div>

//     </div>
//   );
// }

// export default StatisticsCard;




// function StatisticsCard({ statistics }) {
//   return (
//     <div
//       style={{
//         border: "1px solid #ddd",
//         padding: "20px",
//         borderRadius: "10px",
//         marginBottom: "20px",
//       }}
//     >
//       <h2>Statistics</h2>

//       <p><strong>Logs:</strong> {statistics.logsParsed}</p>
//       <p><strong>Errors:</strong> {statistics.errors}</p>
//       <p><strong>Warnings:</strong> {statistics.warnings}</p>
//       <p><strong>Templates:</strong> {statistics.templates}</p>
//       <p><strong>Features:</strong> {statistics.features}</p>
//     </div>
//   );
// }

// export default StatisticsCard;