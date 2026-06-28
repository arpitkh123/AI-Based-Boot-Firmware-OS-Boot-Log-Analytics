function AnalyzeButton({ onAnalyze, disabled }) {
  return (
    <button
      onClick={onAnalyze}
      disabled={disabled}
      style={{
        marginTop: "30px",
        padding: "12px 24px",
        cursor: disabled ? "not-allowed" : "pointer",
      }}
    >
      Analyze Log
    </button>
  );
}

export default AnalyzeButton;