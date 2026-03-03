import React, { useState, useEffect } from "react";
import { embedImageStego, extractImageStego } from "../services/stegoService";
import { processCrypto } from "../services/cryptoService";
import "../styles/steganography.css";

function Stego() {
  /* ================= STATE ================= */

  const [embedAlgorithm, setEmbedAlgorithm] = useState("lsb");
  const [extractAlgorithm, setExtractAlgorithm] = useState("lsb");

  const [embedPassword, setEmbedPassword] = useState("");
  const [extractPassword, setExtractPassword] = useState("");

  const [embedDualLayer, setEmbedDualLayer] = useState(false);
  const [embedCryptoAlgo, setEmbedCryptoAlgo] = useState("aes");

  const [extractDualLayer, setExtractDualLayer] = useState(false);
  const [extractCryptoAlgo, setExtractCryptoAlgo] = useState("aes");

  const [coverImage, setCoverImage] = useState(null);
  const [coverPreview, setCoverPreview] = useState(null);
  const [secret, setSecret] = useState("");

  const [stegoImage, setStegoImage] = useState(null);
  const [stegoPreview, setStegoPreview] = useState(null);

  const [result, setResult] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  /* ================= HELPERS ================= */

  const resetStatus = () => {
    setResult("");
    setError("");
  };

  /* Cleanup object URLs */
  useEffect(() => {
    return () => {
      if (coverPreview) URL.revokeObjectURL(coverPreview);
      if (stegoPreview) URL.revokeObjectURL(stegoPreview);
    };
  }, [coverPreview, stegoPreview]);

  /* ================= EMBED ================= */

  const handleEmbed = async () => {
    resetStatus();

    if (!coverImage || !secret.trim()) {
      setError("Cover image and secret message are required.");
      return;
    }

    if (embedAlgorithm === "lsb-keyed" && !embedPassword) {
      setError("Encryption password required.");
      return;
    }

    try {
      setLoading(true);

      let finalSecret = secret;

      if (embedDualLayer) {
        if (!embedPassword) throw new Error("Encryption key required for Dual-Layer Security.");
        const cRes = await processCrypto(embedCryptoAlgo, "encrypt", secret, embedPassword);
        if (!cRes.data.result) throw new Error("Encryption failed.");
        finalSecret = cRes.data.result;
      }

      const res = await embedImageStego(
        coverImage,
        finalSecret,
        embedAlgorithm,
        embedAlgorithm === "lsb-keyed" ? embedPassword : ""
      );

      const blob = new Blob([res.data], { type: "image/png" });
      const url = URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "deeptrace_stego.png";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      URL.revokeObjectURL(url);

      setResult("Stego image generated successfully.");
    } catch (err) {
      setError(
        err.message ||
        err?.response?.data?.error ||
        "Embedding failed. Check image size or message length."
      );
    } finally {
      setLoading(false);
    }
  };

  /* ================= EXTRACT ================= */

  const handleExtract = async () => {
    resetStatus();

    if (!stegoImage) {
      setError("Please upload a stego image.");
      return;
    }

    if (extractAlgorithm === "lsb-keyed" && !extractPassword) {
      setError("Decryption password required.");
      return;
    }

    try {
      setLoading(true);

      const res = await extractImageStego(
        stegoImage,
        extractAlgorithm,
        extractAlgorithm === "lsb-keyed" ? extractPassword : ""
      );

      let finalMessage = res.data.data.message;

      if (extractDualLayer) {
        if (!extractPassword) throw new Error("Decryption key required for Dual-Layer Security.");

        let cleanText = finalMessage.split('\x00')[0].trim();
        const cRes = await processCrypto(extractCryptoAlgo, "decrypt", cleanText, extractPassword);

        if (!cRes.data.result) throw new Error("Decryption failed or incorrect password.");
        finalMessage = cRes.data.result;
      }

      setResult(`Extracted message: ${finalMessage}`);
    } catch (err) {
      setError(
        err.message ||
        err?.response?.data?.error ||
        "Extraction failed. Wrong password or invalid stego image."
      );
    } finally {
      setLoading(false);
    }
  };

  /* ================= UI ================= */

  return (
    <div className="stego-container">
      {/* HEADER */}
      <div className="stego-header">
        <h1>Image Steganography</h1>
        <p>
          Upload any image format. DeepTrace automatically normalizes it to PNG internally.
        </p>
      </div>

      {/* GRID LAYOUT */}
      <div className="stego-grid">

        {/* ================= EMBED CARD ================= */}
        <div className="stego-card">
          <h2>Embed Message</h2>

          <div className="form-group">
            <label>Algorithm</label>
            <select
              value={embedAlgorithm}
              onChange={(e) => setEmbedAlgorithm(e.target.value)}
            >
              <option value="lsb">LSB (Standard)</option>
              <option value="lsb-keyed">LSB + AES Keyed</option>
            </select>
          </div>

          {(embedAlgorithm === "lsb-keyed" || embedDualLayer) && (
            <div className="form-group">
              <label>{embedDualLayer ? "Encryption Key" : "Encryption Password"}</label>
              <input
                type="password"
                placeholder="Enter password/key"
                value={embedPassword}
                onChange={(e) => setEmbedPassword(e.target.value)}
              />
            </div>
          )}

          <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px', marginTop: '10px' }}>
            <input type="checkbox" id="embedDual" checked={embedDualLayer} onChange={(e) => setEmbedDualLayer(e.target.checked)} style={{ marginRight: '8px', cursor: 'pointer' }} />
            <label htmlFor="embedDual" style={{ margin: 0, fontWeight: 'bold' }}>Enable Dual-Layer Security (Pre-Encrypt)</label>
          </div>

          {embedDualLayer && (
            <div className="form-group">
              <label>Encryption Algorithm</label>
              <select value={embedCryptoAlgo} onChange={(e) => setEmbedCryptoAlgo(e.target.value)}>
                <option value="aes">AES-256</option>
                <option value="3des">Triple DES</option>
                <option value="blowfish">Blowfish</option>
                <option value="chacha20">ChaCha20</option>
                <option value="caesar">Caesar Cipher</option>
              </select>
            </div>
          )}

          <div className="form-group">
            <label>Upload Cover Image</label>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => {
                const file = e.target.files[0];
                if (!file) return;

                resetStatus();
                setCoverImage(file);

                if (coverPreview) URL.revokeObjectURL(coverPreview);
                setCoverPreview(URL.createObjectURL(file));
              }}
            />
          </div>

          {coverPreview && (
            <div className="image-preview">
              <img src={coverPreview} alt="Cover Preview" />
            </div>
          )}

          <div className="form-group">
            <label>Secret Message</label>
            <textarea
              placeholder="Enter message to hide inside image"
              value={secret}
              onChange={(e) => setSecret(e.target.value)}
            />
          </div>

          <button
            className="primary-btn"
            onClick={handleEmbed}
            disabled={loading}
          >
            {loading ? "Processing..." : "Generate Stego Image"}
          </button>
        </div>

        {/* ================= EXTRACT CARD ================= */}
        <div className="stego-card">
          <h2>Extract Message</h2>

          <div className="form-group">
            <label>Algorithm</label>
            <select
              value={extractAlgorithm}
              onChange={(e) => setExtractAlgorithm(e.target.value)}
            >
              <option value="lsb">LSB (Standard)</option>
              <option value="lsb-keyed">LSB + AES Keyed</option>
            </select>
          </div>

          {(extractAlgorithm === "lsb-keyed" || extractDualLayer) && (
            <div className="form-group">
              <label>{extractDualLayer ? "Decryption Key" : "Decryption Password"}</label>
              <input
                type="password"
                placeholder="Enter password/key"
                value={extractPassword}
                onChange={(e) => setExtractPassword(e.target.value)}
              />
            </div>
          )}

          <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px', marginTop: '10px' }}>
            <input type="checkbox" id="extractDual" checked={extractDualLayer} onChange={(e) => setExtractDualLayer(e.target.checked)} style={{ marginRight: '8px', cursor: 'pointer' }} />
            <label htmlFor="extractDual" style={{ margin: 0, fontWeight: 'bold' }}>Enable Dual-Layer Security (Decrypt after Extract)</label>
          </div>

          {extractDualLayer && (
            <div className="form-group">
              <label>Decryption Algorithm</label>
              <select value={extractCryptoAlgo} onChange={(e) => setExtractCryptoAlgo(e.target.value)}>
                <option value="aes">AES-256</option>
                <option value="3des">Triple DES</option>
                <option value="blowfish">Blowfish</option>
                <option value="chacha20">ChaCha20</option>
                <option value="caesar">Caesar Cipher</option>
              </select>
            </div>
          )}

          <div className="form-group">
            <label>Upload Stego Image</label>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => {
                const file = e.target.files[0];
                if (!file) return;

                resetStatus();
                setStegoImage(file);

                if (stegoPreview) URL.revokeObjectURL(stegoPreview);
                setStegoPreview(URL.createObjectURL(file));
              }}
            />
          </div>

          {stegoPreview && (
            <div className="image-preview">
              <img src={stegoPreview} alt="Stego Preview" />
            </div>
          )}

          <button
            className="secondary-btn"
            onClick={handleExtract}
            disabled={loading}
          >
            {loading ? "Processing..." : "Extract Message"}
          </button>
        </div>
      </div>

      {/* STATUS MESSAGE */}
      {(result || error) && (
        <div className={`status-box ${error ? "error" : "success"}`}>
          {error || result}
        </div>
      )}
    </div>
  );
}

export default Stego; 