function FileInput({ onFileSelect }) {
  const handleChange = (event) => {
    const file = event.target.files[0];

    if (file) {
      onFileSelect(file);
    }
  };

  return (
    <input
      type="file"
      accept=".txt,.log"
      onChange={handleChange}
    />
  );
}

export default FileInput;