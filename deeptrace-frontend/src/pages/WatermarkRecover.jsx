import { useState } from "react";
import WatermarkEngine from "../utils/watermark/watermarkEngine";

function WatermarkRecover() {
    const [image, setImage] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);
    const [recoveredData, setRecoveredData] = useState(null);
    const [processing, setProcessing] = useState(false);
    const [error, setError] = useState(null);
    const [showSecretKey, setShowSecretKey] = useState(false);

    // Configuration
    const [type, setType] = useState("invisible_lsb");
    const [secretKey, setSecretKey] = useState("");

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            setImage(file);
            setPreviewUrl(URL.createObjectURL(file));
            setRecoveredData(null);
            setError(null);
        }
    };

    const handleRecover = async () => {
        if (!image) {
            setError("Please upload an image first.");
            return;
        }
        if (!secretKey && type !== "visible") {
            setError("Please enter the secret key used for embedding.");
            return;
        }

        try {
            setProcessing(true);
            setError(null);
            setRecoveredData(null);

            const result = await WatermarkEngine.recoverWatermark(type, image, { secretKey });
            setRecoveredData(result);
        } catch (err) {
            console.error(err);
            setError("Recovery failed: " + err.message);
        } finally {
            setProcessing(false);
        }
    };

    return (
        <div className="page fade-in">
            <h1 className="page-title">Extract Watermark</h1>
            <p className="page-subtitle">
                Extract hidden data from watermarked images.
            </p>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "1fr 1fr",
                    gap: "40px",
                    marginTop: "20px",
                }}
            >
                {/* LEFT: Upload */}
                <div className="card fade-in" style={{ height: "fit-content" }}>
                    <h2 style={{ fontSize: "1.1rem", marginBottom: "16px", color: "var(--text-primary)", display: "flex", alignItems: "center", gap: "10px" }}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ color: "var(--accent)" }}>
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                            <circle cx="8.5" cy="8.5" r="1.5"></circle>
                            <polyline points="21 15 16 10 5 21"></polyline>
                        </svg>
                        1. Upload Watermarked Image
                    </h2>
                    <div className="form-group">
                        <input
                            type="file"
                            accept="image/png, image/jpeg"
                            onChange={handleImageUpload}
                            className="input-field"
                        />
                    </div>
                    {previewUrl && (
                        <div style={{ marginTop: "20px", textAlign: "center" }}>
                            <img
                                src={previewUrl}
                                alt="Preview"
                                style={{
                                    maxWidth: "100%",
                                    maxHeight: "300px",
                                    borderRadius: "var(--radius-sm)",
                                    border: "1px solid var(--border-light)",
                                }}
                            />
                        </div>
                    )}
                </div>

                {/* RIGHT: Controls & Result */}
                <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>

                    <div className="card fade-in">
                        <h2 style={{ fontSize: "1.1rem", marginBottom: "16px", color: "var(--text-primary)", display: "flex", alignItems: "center", gap: "10px" }}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ color: "var(--accent)" }}>
                                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                            </svg>
                            2. Security Settings
                        </h2>

                        <div className="form-group">
                            <label>Extraction Method</label>
                            <select
                                value={type}
                                onChange={(e) => setType(e.target.value)}
                                className="input-field"
                            >
                                <option value="invisible_lsb">Invisible (LSB)</option>
                                <option value="invisible_dct">Invisible (DCT)</option>
                                <option value="invisible_dwt">Invisible (DWT)</option>
                                <option value="visible">Visible Watermark</option>
                            </select>
                        </div>

                        {type !== "visible" && (
                            <div className="form-group">
                                <label>Secret Key</label>
                                <div style={{ position: "relative" }}>
                                    <input
                                        type={showSecretKey ? "text" : "password"}
                                        placeholder="Enter the key used during embedding..."
                                        value={secretKey}
                                        onChange={(e) => setSecretKey(e.target.value)}
                                        className="input-field"
                                        style={{ paddingRight: "40px", width: "100%" }}
                                    />
                                    <button
                                        type="button"
                                        onClick={() => setShowSecretKey(!showSecretKey)}
                                        style={{
                                            position: "absolute",
                                            right: "10px",
                                            top: "0",
                                            height: "100%",
                                            background: "none",
                                            border: "none",
                                            color: "var(--text-secondary)",
                                            cursor: "pointer",
                                            padding: "0 4px",
                                            display: "flex",
                                            alignItems: "center",
                                            justifyContent: "center"
                                        }}
                                        aria-label={showSecretKey ? "Hide key" : "Show key"}
                                    >
                                        {showSecretKey ? (
                                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                                                <line x1="1" y1="1" x2="23" y2="23"></line>
                                            </svg>
                                        ) : (
                                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                                <circle cx="12" cy="12" r="3"></circle>
                                            </svg>
                                        )}
                                    </button>
                                </div>
                            </div>
                        )}

                        {error && <div className="error-box" style={{ marginTop: "15px" }}>{error}</div>}

                        <button
                            onClick={handleRecover}
                            disabled={processing || !image}
                            className="btn-primary"
                            style={{ width: "100%", marginTop: "20px" }}
                        >
                            {processing ? "Extracting..." : "Extract Data"}
                        </button>
                    </div>

                    {/* Results Box */}
                    {recoveredData && (
                        <div className="card fade-in">
                            <h2 style={{ fontSize: "1.1rem", marginBottom: "16px", color: recoveredData.isValid ? "var(--accent-success)" : "var(--accent)" }}>
                                {recoveredData.isValid ? "✓ Verification Successful" : "⚠ Verification Failed"}
                            </h2>

                            <div style={{
                                background: "var(--bg-main)",
                                padding: "15px",
                                borderRadius: "var(--radius-sm)",
                                border: "1px solid var(--border-light)"
                            }}>
                                <div style={{ display: "grid", gap: "12px" }}>

                                    {/* Integrity Badge */}
                                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                                        <span style={{ color: "var(--text-secondary)" }}>Integrity Check</span>
                                        <span style={{
                                            padding: "4px 8px",
                                            borderRadius: "4px",
                                            background: recoveredData.isValid ? "rgba(16, 185, 129, 0.1)" : "rgba(239, 68, 68, 0.1)",
                                            color: recoveredData.isValid ? "#10b981" : "#ef4444",
                                            fontWeight: "bold",
                                            fontSize: "0.9rem"
                                        }}>
                                            {recoveredData.isValid ? "VALID SIGNATURE" : "INVALID / TAMPERED"}
                                        </span>
                                    </div>

                                    {recoveredData.isValid ? (
                                        <>
                                            {recoveredData.text && (
                                                <div style={{ display: "flex", justifyContent: "space-between" }}>
                                                    <span style={{ color: "var(--text-secondary)" }}>Watermark Text</span>
                                                    <span style={{ color: "var(--text-primary)", fontWeight: "bold" }}>
                                                        {recoveredData.text}
                                                    </span>
                                                </div>
                                            )}

                                            <div style={{ display: "flex", justifyContent: "space-between" }}>
                                                <span style={{ color: "var(--text-secondary)" }}>User ID</span>
                                                <span style={{ fontFamily: "monospace", color: "var(--text-primary)" }}>
                                                    {recoveredData.userId}
                                                </span>
                                            </div>

                                            <div style={{ display: "flex", justifyContent: "space-between" }}>
                                                <span style={{ color: "var(--text-secondary)" }}>Timestamp</span>
                                                <span style={{ color: "var(--text-primary)" }}>
                                                    {recoveredData.timestamp}
                                                </span>
                                            </div>

                                            <div style={{ marginTop: "10px", padding: "10px", background: "#f8fafc", borderRadius: "4px" }}>
                                                <small style={{ display: "block", color: "#64748b", marginBottom: "4px" }}>Raw Payload Hash</small>
                                                <code style={{ wordBreak: "break-all", fontSize: "0.8rem", color: "#334155" }}>
                                                    {recoveredData.decoded?.hash || "N/A"}
                                                </code>
                                            </div>
                                        </>
                                    ) : (
                                        <div style={{ color: "var(--text-secondary)", fontStyle: "italic" }}>
                                            <p>The extracted data could not be verified. This usually means:</p>
                                            <ul style={{ paddingLeft: "20px", marginTop: "8px" }}>
                                                <li>The image has been tampered with (cropped, resized, compressed)</li>
                                                <li>The wrong secret key was provided</li>
                                                <li>The image does not contain a watermark</li>
                                            </ul>

                                            {recoveredData.raw && (
                                                <div style={{ marginTop: "15px" }}>
                                                    <small>Raw Extracted Data Dump:</small>
                                                    <pre style={{
                                                        marginTop: "5px",
                                                        padding: "8px",
                                                        background: "#f1f5f9",
                                                        overflow: "auto",
                                                        fontSize: "0.8rem"
                                                    }}>
                                                        {recoveredData.raw.substring(0, 200)}...
                                                    </pre>
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default WatermarkRecover;
