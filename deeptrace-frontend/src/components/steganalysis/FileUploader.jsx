import { useState } from "react";
import "../../styles/steganalysis.css";

function FileUploader({ onFileSelect }) {
  const [fileName, setFileName] = useState("");
  const [error, setError] = useState("");

  const supportedExtensions = [
    "jpg", "jpeg", "png", "bmp", "tiff", "webp",
    "txt", "pdf", "docx", "zip", "bin"
  ];

  const handleFileChange = (e) => {
    const file = e.target.files[0];

    if (!file) return;

    const extension = file.name.split(".").pop().toLowerCase();

    if (!supportedExtensions.includes(extension)) {
      setError("Unsupported file format.");
      setFileName("");
      onFileSelect(null);
      return;
    }

    setError("");
    setFileName(file.name);
    onFileSelect(file);
  };

  return (
    <div className="upload-box">
      
      <input
        type="file"
        onChange={handleFileChange}
      />

      <p>
        <strong>Supported Formats:</strong>
        <br />
        Images: JPG, PNG, BMP, TIFF, WEBP
        <br />
        Files: TXT, PDF, DOCX, ZIP, BIN
      </p>

      {fileName && (
        <p className="upload-selected">
          Selected File: {fileName}
        </p>
      )}

      {error && (
        <p className="upload-error">
          {error}
        </p>
      )}
    </div>
  );
}

export default FileUploader;