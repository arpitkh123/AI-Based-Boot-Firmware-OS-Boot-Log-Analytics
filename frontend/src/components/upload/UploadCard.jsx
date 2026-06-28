function UploadCard({ children }) {
  return (

    <div className="max-w-2xl mx-auto mt-16 p-8 bg-blue-100 rounded-xl shadow-lg">
      {children}
    </div>



    // <div
    //   style={{
    //     maxWidth: "700px",
    //     margin: "60px auto",
    //     padding: "30px",
    //     border: "1px solid #ddd",
    //     borderRadius: "12px",
    //     background: "#fff",
    //     boxShadow: "0 2px 10px rgba(0,0,0,0.08)",
    //   }}
    // >
    //   {children}
    // </div>
  );
}

export default UploadCard;