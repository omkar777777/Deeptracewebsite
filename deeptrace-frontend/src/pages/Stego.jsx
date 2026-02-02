import React, { useState } from "react";
import { embedTextStego, extractTextStego } from "../services/stegoService";
import "../styles/steganography.css";

function Stego() {
  const [algorithm, setAlgorithm] = useState("zerowidth");
  const [coverText, setCoverText] = useState("");
  const [secret, setSecret] = useState("");
  const [stegoFile, setStegoFile] = useState(null);

  const [result, setResult] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const reset = () => {
    setResult("");
    setError("");
  };

  /* ================= EMBED ================= */

  const handleEmbed = async () => {
    if (!coverText || !secret) {
      setError("Cover text and secret message are required.");
      return;
    }

    try {
      setLoading(true);
      reset();

      const res = await embedTextStego(coverText, secret, algorithm);

      // ✅ CORRECT: convert ArrayBuffer → Blob
      const blob = new Blob(
        [res.data],
        { type: "text/plain;charset=utf-8" }
      );

      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "stego.txt";
      a.click();

      URL.revokeObjectURL(url);

      setResult("Stego text file downloaded successfully.");
    } catch (e) {
      setError("Embedding failed. Check cover text length / algorithm.");
    } finally {
      setLoading(false);
    }
  };

  /* ================= EXTRACT ================= */

  const handleExtract = async () => {
    if (!stegoFile) {
      setError("Please upload a stego text file.");
      return;
    }

    try {
      setLoading(true);
      reset();

      const res = await extractTextStego(stegoFile, algorithm);
      setResult(`Extracted message: ${res.data.data.message}`);
    } catch (e) {
      setError("Extraction failed. Wrong algorithm or invalid stego file.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="stego-page">
      <h1>Text Steganography</h1>

      <div className="stego-warning">
        ⚠ File-based steganography. Preview disabled to preserve data.
      </div>

      <label>Algorithm</label>
      <select value={algorithm} onChange={e => setAlgorithm(e.target.value)}>
        <option value="zerowidth">Zero Width</option>
        <option value="whitespace">Whitespace</option>
      </select>

      <label>Cover Text</label>
      <textarea
        placeholder="Paste cover text here"
        value={coverText}
        onChange={e => setCoverText(e.target.value)}
      />

      <label>Secret Message</label>
      <textarea
        placeholder="Message to hide"
        value={secret}
        onChange={e => setSecret(e.target.value)}
      />

      <button onClick={handleEmbed} disabled={loading}>
        Embed → Download stego.txt
      </button>

      <hr />

      <label>Upload Stego Text File</label>
      <input
        type="file"
        accept=".txt"
        onChange={e => setStegoFile(e.target.files[0])}
      />

      <button onClick={handleExtract} disabled={loading || !stegoFile}>
        Extract Message
      </button>

      <div className="stego-output">
        {loading && "Processing..."}
        {!loading && result}
        {!loading && error && <div className="stego-error">{error}</div>}
      </div>
    </div>
  );
}

export default Stego;