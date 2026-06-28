function RecommendationCard({ recommendation }) {
  return (
    <div className="card bg-base-100 shadow">

      <div className="card-body">

        <h2 className="card-title">
          AI Recommendation
        </h2>

        <div className="alert alert-error">

          <div>

            <h3 className="font-bold">
              Root Cause
            </h3>

            <p>
              {recommendation.rootCause}
            </p>

          </div>

        </div>

        <div className="alert alert-info mt-4">

          <div>

            <h3 className="font-bold">
              Reason
            </h3>

            <p>
              {recommendation.reason}
            </p>

          </div>

        </div>

        <div className="alert alert-success mt-4">

          <div>

            <h3 className="font-bold">
              Suggested Resolution
            </h3>

            <p>
              {recommendation.solution}
            </p>

          </div>

        </div>

      </div>

    </div>
  );
}

export default RecommendationCard;




// function RecommendationCard({ recommendation }) {
//   return (
//     <div className="card bg-base-100 shadow mb-6">

//       <div className="card-body">

//         <h2 className="card-title">
//           AI Recommendation
//         </h2>

//         <div className="divider"></div>

//         <h3 className="font-bold">
//           Root Cause
//         </h3>

//         <p>
//           {recommendation.rootCause}
//         </p>

//         <h3 className="font-bold mt-4">
//           Reason
//         </h3>

//         <p>
//           {recommendation.reason}
//         </p>

//         <h3 className="font-bold mt-4">
//           Suggested Resolution
//         </h3>

//         <p>
//           {recommendation.solution}
//         </p>

//       </div>

//     </div>
//   );
// }

// export default RecommendationCard;





// function RecommendationCard({ recommendation }) {
//   return (
//     <div
//       style={{
//         border: "1px solid #ddd",
//         padding: "20px",
//         borderRadius: "10px",
//         marginBottom: "20px",
//       }}
//     >
//       <h2>Recommendation</h2>

//       <p><strong>Root Cause:</strong> {recommendation.rootCause}</p>

//       <p><strong>Reason:</strong> {recommendation.reason}</p>

//       <p><strong>Solution:</strong> {recommendation.solution}</p>
//     </div>
//   );
// }

// export default RecommendationCard;