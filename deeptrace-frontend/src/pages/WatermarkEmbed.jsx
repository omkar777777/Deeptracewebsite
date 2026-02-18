import { useState } from "react";
import WatermarkEngine from "../utils/watermark/watermarkEngine";

function WatermarkEmbed() {
    const [image, setImage] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);
    const [resultUrl, setResultUrl] = useState(null);
    const [processing, setProcessing] = useState(false);
    const [error, setError] = useState(null);
    const [showSecretKey, setShowSecretKey] = useState(false);

    // Configuration State
    const [type, setType] = useState("invisible_lsb"); // visible, invisible_lsb, invisible_dct, invisible_dwt
    const [options, setOptions] = useState({
        text: "",
        opacity: 0.5,
        fontSize: 40,
        position: "center",
        secretKey: "",
    });

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            setImage(file);
            setPreviewUrl(URL.createObjectURL(file));
            setResultUrl(null);
            setError(null);
        }
    };

    const handleOptionChange = (key, value) => {
        setOptions((prev) => ({ ...prev, [key]: value }));
    };

    const handleApplyWatermark = async () => {
        if (!image) {
            setError("Please upload an image first.");
            return;
        }

        try {
            setProcessing(true);
            setError(null);

            const result = await WatermarkEngine.applyWatermark(type, image, options);
            setResultUrl(result.dataUrl);
        } catch (err) {
            console.error(err);
            setError(err.message);
        } finally {
            setProcessing(false);
        }
    };

    return (
        <div className="page fade-in">
            <h1 className="page-title">Embed Watermark</h1>
            <p className="page-subtitle">
                Secure your images with visible or invisible watermarks.
            </p>

            {/* Main Container - Adjusted for horizontal alignment in rows */}
            <div style={{ marginTop: "20px", display: "flex", flexDirection: "column", gap: "30px" }}>

                {/* ROW 1: Configuration Selection (Type & Settings) */}
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "40px" }}>

                    {/* Box 1: Watermark Type */}
                    <div className="card fade-in">
                        <h2
                            style={{
                                fontSize: "1.1rem",
                                marginBottom: "16px",
                                color: "var(--text-primary)",
                                display: "flex",
                                alignItems: "center",
                                gap: "10px"
                            }}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ color: "var(--accent)" }}>
                                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                                <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                                <line x1="12" y1="22.08" x2="12" y2="12"></line>
                            </svg>
                            1. Select Watermark Type
                        </h2>
                        <div className="form-group">
                            <select
                                value={type}
                                onChange={(e) => setType(e.target.value)}
                                className="input-field"
                                style={{ fontSize: "1rem", padding: "10px" }}
                            >
                                <option value="visible">Visible Watermark (Overlay)</option>
                                <option value="invisible_lsb">Invisible (LSB - Stealth)</option>
                                <option value="invisible_dct">Invisible (DCT - Robust)</option>
                                <option value="invisible_dwt">Invisible (DWT - Wavelet)</option>
                            </select>
                        </div>
                        <p style={{ fontSize: "0.9rem", color: "var(--text-secondary)" }}>
                            {type === "visible"
                                ? "Add a visible text overlay to your image. Great for copyright."
                                : "Hide data imperceptibly using steganographic techniques."}
                        </p>
                    </div>

                    {/* Box 2: Configure Settings */}
                    <div className="card fade-in">
                        <h2
                            style={{
                                fontSize: "1.1rem",
                                marginBottom: "16px",
                                color: "var(--text-primary)",
                                display: "flex",
                                alignItems: "center",
                                gap: "10px"
                            }}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ color: "var(--accent)" }}>
                                <circle cx="12" cy="12" r="3"></circle>
                                <path d="M12 1v6m0 6v6m5.2-13.2l-4.2 4.2m0 6l-4.2 4.2M23 12h-6m-6 0H5m13.2 5.2l-4.2-4.2m0-6l-4.2-4.2"></path>
                            </svg>
                            2. Configure Settings
                        </h2>

                        {/* Unified Settings Grid */}
                        <div className="fade-in">
                            <div style={{ display: "grid", gridTemplateColumns: type.startsWith("invisible") ? "1fr 1fr" : "1fr", gap: "20px", alignItems: "start" }}>

                                {/* 1. Watermark Text */}
                                <div className="form-group">
                                    <label>Watermark Text {type !== "visible" && "(Optional)"}</label>
                                    <input
                                        type="text"
                                        value={options.text}
                                        onChange={(e) => handleOptionChange("text", e.target.value)}
                                        className="input-field"
                                        placeholder={type === "visible" ? "e.g. My Name" : "Hidden secret message..."}
                                    />
                                </div>

                                {/* 2. Secret Key (Invisible Only) */}
                                {type.startsWith("invisible") && (
                                    <div className="form-group">
                                        <label>Secret Key</label>
                                        <div style={{ position: "relative" }}>
                                            <input
                                                type={showSecretKey ? "text" : "password"}
                                                placeholder="Enter a secure key..."
                                                value={options.secretKey}
                                                onChange={(e) =>
                                                    handleOptionChange("secretKey", e.target.value)
                                                }
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
                                        <small
                                            style={{
                                                display: "block",
                                                marginTop: "6px",
                                                color: "var(--text-secondary)",
                                                fontStyle: "italic",
                                                fontSize: "0.8rem"
                                            }}
                                        >
                                            Key used for randomized embedding.
                                        </small>
                                    </div>
                                )}
                            </div>

                            {/* 3. Visible Options (Visible Only) */}
                            {type === "visible" && (
                                <div style={{ marginTop: "20px", display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
                                    <div className="form-group">
                                        <label>Position</label>
                                        <select
                                            value={options.position}
                                            onChange={(e) =>
                                                handleOptionChange("position", e.target.value)
                                            }
                                            className="input-field"
                                        >
                                            <option value="center">Center</option>
                                            <option value="topLeft">Top Left</option>
                                            <option value="topRight">Top Right</option>
                                            <option value="bottomLeft">Bottom Left</option>
                                            <option value="bottomRight">Bottom Right</option>
                                        </select>
                                    </div>
                                    <div className="form-group">
                                        <label>Opacity ({Math.round(options.opacity * 100)}%)</label>
                                        <div style={{ display: "flex", alignItems: "center", height: "42px" }}>
                                            <input
                                                type="range"
                                                min="0.1"
                                                max="1"
                                                step="0.05"
                                                value={options.opacity}
                                                onChange={(e) =>
                                                    handleOptionChange("opacity", parseFloat(e.target.value))
                                                }
                                                style={{ width: "100%", accentColor: "var(--accent)", cursor: "pointer" }}
                                            />
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* ROW 2: Image Operations (Upload & Process) - ALIGNED */}
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "40px" }}>

                    {/* Box 3: Image Upload */}
                    <div className="card fade-in" style={{ height: "100%", display: "flex", flexDirection: "column" }}>
                        <h2
                            style={{
                                fontSize: "1.1rem",
                                marginBottom: "16px",
                                color: "var(--text-primary)",
                                display: "flex",
                                alignItems: "center",
                                gap: "10px"
                            }}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ color: "var(--accent)" }}>
                                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                                <circle cx="8.5" cy="8.5" r="1.5"></circle>
                                <polyline points="21 15 16 10 5 21"></polyline>
                            </svg>
                            3. Upload Source Image
                        </h2>
                        <div className="form-group">
                            <label>Select JPEG or PNG</label>
                            <input
                                type="file"
                                accept="image/png, image/jpeg"
                                onChange={handleImageUpload}
                                className="input-field"
                            />
                        </div>

                        {previewUrl && (
                            <div
                                className="fade-in"
                                style={{
                                    marginTop: "auto",
                                    paddingTop: "20px",
                                    textAlign: "center",
                                    flex: 1,
                                    display: "flex",
                                    alignItems: "center",
                                    justifyContent: "center"
                                }}
                            >
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

                    {/* Box 4: Process Image */}
                    <div className="card fade-in" style={{ height: "100%", display: "flex", flexDirection: "column" }}>
                        <h2
                            style={{
                                fontSize: "1.1rem",
                                marginBottom: "16px",
                                color: "var(--text-primary)",
                                display: "flex",
                                alignItems: "center",
                                gap: "10px"
                            }}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ color: "var(--accent)" }}>
                                <polyline points="16 18 22 12 16 6"></polyline>
                                <polyline points="8 6 2 12 8 18"></polyline>
                            </svg>
                            4. Process Image
                        </h2>

                        {error && <div className="error-box">{error}</div>}

                        <button
                            onClick={handleApplyWatermark}
                            disabled={processing || !image}
                            className="btn-primary"
                            style={{ width: "100%", marginBottom: resultUrl ? "20px" : "0" }}
                        >
                            {processing ? "Processing..." : "Apply Watermark"}
                        </button>

                        {/* Result Preview */}
                        {resultUrl && (
                            <div
                                className="fade-in"
                                style={{
                                    marginTop: "auto",
                                    paddingTop: "20px",
                                    borderTop: "1px solid var(--border-light)",
                                    textAlign: "center",
                                    flex: 1,
                                    display: "flex",
                                    flexDirection: "column",
                                    alignItems: "center",
                                    justifyContent: "center"
                                }}
                            >
                                <p
                                    style={{
                                        marginBottom: "10px",
                                        fontWeight: "bold",
                                        color: "var(--accent)",
                                    }}
                                >
                                    ✓ Watermark Applied Successfully
                                </p>
                                <img
                                    src={resultUrl}
                                    alt="Result"
                                    style={{
                                        maxWidth: "100%",
                                        maxHeight: "300px",
                                        borderRadius: "var(--radius-sm)",
                                        border: "1px solid var(--border-light)",
                                        marginBottom: "15px",
                                    }}
                                />
                                <br />
                                <div style={{
                                    border: "1px solid var(--border-light)",
                                    borderRadius: "var(--radius-sm)",
                                    padding: "15px",
                                    background: "var(--bg-main)",
                                    width: "fit-content",
                                    margin: "0 auto",
                                    display: "flex",
                                    flexDirection: "column",
                                    gap: "8px"
                                }}>
                                    <a
                                        href={resultUrl}
                                        download={`watermarked_${Date.now()}.png`}
                                        className="btn-secondary"
                                        style={{ display: "inline-block", width: "100%" }}
                                    >
                                        Download Image
                                    </a>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default WatermarkEmbed;
