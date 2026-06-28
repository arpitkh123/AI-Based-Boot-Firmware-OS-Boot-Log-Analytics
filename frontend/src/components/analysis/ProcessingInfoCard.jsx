function ProcessingInfoCard({
  processing,
  statistics,
  analysisId,
}) {
  return (
    <div className="card bg-base-100 shadow h-full">

      <div className="card-body">

        <h2 className="card-title">
          Processing
        </h2>

        <p>
          <strong>Analysis ID:</strong>{" "}
          {analysisId}
        </p>

        <p>
          <strong>Time:</strong>{" "}
          {processing.time}s
        </p>

        <p>
          <strong>Logs Parsed:</strong>{" "}
          {statistics.logsParsed}
        </p>

      </div>

    </div>
  );
}

export default ProcessingInfoCard;