function PredictionCard({ prediction, bootStatus }) {
  return (
    <div className="hero bg-base-100 rounded-xl shadow mb-6">

      <div className="hero-content w-full">

        <div className="w-full flex justify-between items-center">

          <div>

            <p className="text-sm uppercase opacity-60">
              Prediction
            </p>

            <h1 className="text-5xl font-bold mt-2">
              {prediction.class}
            </h1>

            <div className="mt-4">

              <div
                className={`badge ${
                  bootStatus
                    ? "badge-success"
                    : "badge-error"
                } badge-lg`}
              >
                {bootStatus
                  ? "BOOT SUCCESSFUL"
                  : "BOOT FAILED"}
              </div>

            </div>

          </div>

          <div className="text-center">

            <div
              className="radial-progress text-error"
              style={{ "--value": prediction.confidence }}
              role="progressbar"
            >
              {prediction.confidence}%
            </div>

            <p className="mt-3 font-semibold">
              Confidence
            </p>

          </div>

        </div>

      </div>

    </div>
  );
}

export default PredictionCard;





// function PredictionCard({ prediction, bootStatus }) {
//   return (
//     <div className="card bg-base-100 shadow mb-6">

//       <div className="card-body">

//         <div className="flex justify-between items-center">

//           <div>

//             <p className="text-sm opacity-70">
//               Prediction
//             </p>

//             <h2 className="text-3xl font-bold">
//               {prediction.class}
//             </h2>

//           </div>

//           <div className="text-right">

//             <div className="badge badge-error mb-2">
//               {bootStatus ? "SUCCESS" : "FAILED"}
//             </div>

//             <p>
//               Confidence
//             </p>

//             <p className="text-2xl font-bold">
//               {prediction.confidence}%
//             </p>

//           </div>

//         </div>

//       </div>

//     </div>
//   );
// }

// export default PredictionCard;





// import Card from "../shared/Card";
// import StatItem from "../shared/StatItem";

// function PredictionCard({ prediction }) {
//   return (
//     <Card>
//       <h2 className="text-2xl font-semibold mb-4">
//         Prediction
//       </h2>

//       <StatItem
//         label="Class"
//         value={prediction.class}
//       />

//       <StatItem
//         label="Confidence"
//         value={`${prediction.confidence}%`}
//       />
//     </Card>
//   );
// }

// export default PredictionCard;




// function PredictionCard({ prediction }) {
//   return (
//     <div
//       style={{
//         border: "1px solid #ddd",
//         padding: "20px",
//         borderRadius: "10px",
//         marginBottom: "20px",
//       }}
//     >
//       <h2>Prediction</h2>

//       <p>
//         <strong>Class:</strong>{" "}
//         {prediction.class}
//       </p>

//       <p>
//         <strong>Confidence:</strong>{" "}
//         {prediction.confidence}%
//       </p>
//     </div>
//   );
// }

// export default PredictionCard;