function FileInfo({ file }) {
  if (!file) return null;

  return (
    <div
      style={{
        marginTop: "20px",
      }}
    >
      <h3>Selected File</h3>

      <p>
        <strong>Name:</strong> {file.name}
      </p>

      <p>
        <strong>Size:</strong>{" "}
        {(file.size / 1024).toFixed(2)} KB
      </p>
    </div>
  );
}

export default FileInfo;