function BootSummaryCard({ boot }) {
  return (
    <div className="card bg-base-100 shadow h-full">

      <div className="card-body">

        <h2 className="card-title">
          Boot Summary
        </h2>

        <p>
          <strong>Status:</strong>{" "}
          {boot.bootSuccessful ? "Successful" : "Failed"}
        </p>

        <p>
          <strong>Failure Stage:</strong>{" "}
          {boot.failureStage}
        </p>

        <p>
          <strong>Duration:</strong>{" "}
          {boot.bootDuration} ms
        </p>

      </div>

    </div>
  );
}

export default BootSummaryCard;




// function BootSummaryCard({ boot }) {
//   return (
//     <div
//       style={{
//         border: "1px solid #ddd",
//         padding: "20px",
//         borderRadius: "10px",
//         marginBottom: "20px",
//       }}
//     >
//       <h2>Boot Summary</h2>

//       <p>
//         <strong>Status:</strong>{" "}
//         {boot.bootSuccessful ? "Success" : "Failed"}
//       </p>

//       <p>
//         <strong>Duration:</strong> {boot.bootDuration} ms
//       </p>

//       <p>
//         <strong>Failure Stage:</strong> {boot.failureStage}
//       </p>
//     </div>
//   );
// }

// export default BootSummaryCard;