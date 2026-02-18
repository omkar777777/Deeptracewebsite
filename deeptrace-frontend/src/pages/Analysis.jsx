import { useState } from "react";
import { analyzeFile } from "../services/steganalysisService";

import {
  FileUploader,
  RiskMeter,
  ScoreBreakdown
} from "../components/steganalysis";

import "../styles/steganalysis.css";

function Analysis() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setResult(null);
    setError("");
    setCopied(false);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError("Please upload a file first.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);
      setCopied(false);

      const response = await analyzeFile(selectedFile);
      setResult(response);
    } catch (err) {
      setError(err.message || "Analysis failed.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(result.extracted_content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Copy failed:", err);
    }
  };

  return (
    <div className="steganalysis-container">
      <h1>Steganalysis Module</h1>

      <FileUploader onFileSelect={handleFileSelect} />

      <button
        className="analyze-btn"
        onClick={handleAnalyze}
        disabled={loading || !selectedFile}
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {error && (
        <p className="upload-error">
          {error}
        </p>
      )}

      {result && (
        <>
          <RiskMeter score={result.total_score} />

          <div style={{ textAlign: "center", marginTop: "15px" }}>
            <strong>Risk Level:</strong> {result.risk_level}
          </div>

          {/* Extraction Result Section */}
          <div style={{ marginTop: "30px" }}>
            {result.hidden_content_found ? (
              <div
                style={{
                  backgroundColor: "#5A2E1F",
                  padding: "20px",
                  borderRadius: "10px",
                  wordWrap: "break-word"
                }}
              >
                <h3 style={{ marginBottom: "10px" }}>
                  Extracted Content:
                </h3>

                <pre style={{ whiteSpace: "pre-wrap" }}>
                  {result.extracted_content}
                </pre>

                <button
                  className="analyze-btn"
                  style={{ marginTop: "15px" }}
                  onClick={handleCopy}
                >
                  {copied ? "Copied!" : "Copy to Clipboard"}
                </button>
              </div>
            ) : (
              <div
                style={{
                  backgroundColor: "#2B1B17",
                  padding: "15px",
                  borderRadius: "8px",
                  marginTop: "10px"
                }}
              >
                {result.message}
              </div>
            )}
          </div>

          <ScoreBreakdown details={result.details} />
        </>
      )}
    </div>
  );
}

export default Analysis;