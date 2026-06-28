import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Upload, FileText } from "lucide-react";

function UploadPage() {
  const navigate = useNavigate();

  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];

    if (!file) return;

    setSelectedFile(file);
  };

  const handleAnalyze = () => {
    navigate("/processing", {
      state: {
        file: selectedFile,
      },
    });
  };

  return (
    <div className="min-h-screen bg-base-200 flex items-center justify-center p-6">
      <div className="card w-full max-w-3xl bg-base-100 shadow-xl">

        <div className="card-body">

          <div className="text-center">

            <h1 className="text-4xl font-bold">
              AI Boot Log Analytics
            </h1>

            <p className="mt-3 text-base-content/70">
              Intelligent Boot Firmware & OS Boot Failure Detection
            </p>

          </div>

          <div className="divider"></div>

          <label
            htmlFor="log-file"
            className="border-2 border-dashed rounded-xl p-12 cursor-pointer hover:border-primary transition"
          >
            <div className="flex flex-col items-center gap-4">

              <Upload size={50} />

              <h2 className="text-xl font-semibold">
                Upload Boot Log
              </h2>

              <p className="text-sm opacity-70">
                Drag & Drop or Click to Browse
              </p>

              <p className="text-xs opacity-60">
                Supported: .txt .log
              </p>

            </div>
          </label>

          <input
            id="log-file"
            type="file"
            accept=".txt,.log"
            className="hidden"
            onChange={handleFileChange}
          />

          {selectedFile && (

            <div className="alert alert-info mt-4">

              <FileText />

              <div>

                <h3 className="font-bold">
                  {selectedFile.name}
                </h3>

                <div className="text-xs">

                  {(selectedFile.size / 1024).toFixed(2)} KB

                </div>

              </div>

            </div>

          )}

          <button
            className="btn btn-primary mt-6"
            disabled={!selectedFile}
            onClick={handleAnalyze}
          >
            Analyze Boot Log
          </button>

        </div>

      </div>
    </div>
  );
}

export default UploadPage;





// import { useState } from "react";
// import { useNavigate } from "react-router-dom";

// import UploadCard from "../../components/upload/UploadCard";
// import FileInput from "../../components/upload/FileInput";
// import FileInfo from "../../components/upload/FileInfo";
// import AnalyzeButton from "../../components/upload/AnalyzeButton";
// // import { analyzeLog } from "../../services/analysisService";


// function Upload() {
//   const [selectedFile, setSelectedFile] = useState(null);

//   const navigate = useNavigate();


//   const handleAnalyze = () => {
//     navigate("/processing", {
//             state: {
//             file: selectedFile,
//             },
//         });
//     };


// //   const handleAnalyze = async () => {
// //     try {
// //         console.log("Uploading...");

// //         navigate("/processing", {
// //             state: {
// //                 file: selectedFile,
// //             },
// //         });

// //         // const result = await analyzeLog(selectedFile);

// //         // console.log(result);

// //         // navigate("/processing");

// //     } catch (error) {

// //             console.error(error);

// //             alert("Unable to connect to backend.");
// //         }
// //     };

// //   const handleAnalyze = () => {
// //     console.log(selectedFile);

// //     navigate("/processing");
// //   };

// //   return (
// //     <UploadCard>
// //       <h1>AI Boot Log Analytics</h1>

// //       <p>Upload a Linux Boot Log for Analysis</p>

// //       <FileInput onFileSelect={setSelectedFile} />

// //       <FileInfo file={selectedFile} />

// //       <AnalyzeButton
// //         onAnalyze={handleAnalyze}
// //         disabled={!selectedFile}
// //       />
// //     </UploadCard>
// //   );

//     return (
//     <div className="hero min-h-screen">
//         <div className="hero-content text-center">
//         <div>
//             <h1 className="text-5xl font-bold">
//             AI Boot Log Analytics
//             </h1>

//             <p className="py-6">
//             Intelligent Linux Boot Failure Analysis
//             </p>

//             <button className="btn btn-primary">
//             DaisyUI Working
//             </button>
//         </div>
//         </div>
//     </div>
//     );

// }

// export default Upload;




// // function Upload() {
// //     return <h1>Upload Page</h1>;
// // }

// // export default Upload;