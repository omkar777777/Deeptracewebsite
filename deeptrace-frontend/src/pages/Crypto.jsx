import { useState } from "react";
import "../styles/crypto.css";

const CAESAR_SHIFT = 3;

function Crypto() {
  const [algorithm, setAlgorithm] = useState("caesar");
  const [text, setText] = useState("");
  const [key, setKey] = useState("");
  const [showKey, setShowKey] = useState(false);
  const [action, setAction] = useState("encrypt");
  const [result, setResult] = useState("");
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setError("");
    setResult("");
    setCopied(false);
    setLoading(true);

    try {
      const payload = { algorithm, action, text };

      // =====================
      // Caesar
      // =====================
      if (algorithm === "caesar") {
        payload.key = CAESAR_SHIFT;
      }

      // =====================
      // Symmetric ciphers
      // AES / DES / 3DES / Blowfish / RC4 / ChaCha20
      // =====================
      if (
        algorithm === "aes" ||
        algorithm === "des" ||
        algorithm === "3des" ||
        algorithm === "blowfish" ||
        algorithm === "rc4" ||
        algorithm === "chacha20"
      ) {
        if (!key) {
          setError(`Passphrase is required for ${algorithm.toUpperCase()}`);
          setLoading(false);
          return;
        }
        payload.key = key;
      }

      // =====================
      // RSA
      // =====================
      if (algorithm === "rsa") {
        if (action !== "generate" && !key) {
          setError(
            action === "encrypt"
              ? "Public key is required for RSA encryption"
              : "Private key is required for RSA decryption"
          );
          setLoading(false);
          return;
        }
        if (action !== "generate") payload.key = key;
      }

      const response = await fetch("http://127.0.0.1:5000/api/crypto", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Something went wrong");
      } else {
        if (algorithm === "rsa" && action === "generate") {
          const content = `RSA KEY PAIR (2048-bit)

PUBLIC KEY:
${data.result.public_key}

PRIVATE KEY:
${data.result.private_key}
`;

          const blob = new Blob([content], { type: "text/plain" });
          const url = URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = "rsa_keys.txt";
          a.click();
          URL.revokeObjectURL(url);

          setKey(data.result.public_key);
          setResult("RSA keys generated and downloaded successfully.");
        } else {
          setResult(data.result);
        }
      }
    } catch {
      setError("Cannot connect to backend");
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = async () => {
    if (!result) return;
    await navigator.clipboard.writeText(result);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <div className="crypto-page">
      {/* Header */}
      <div className="crypto-header">
        <div>
          <h1>Cryptography</h1>
          <p>Algorithm-based encryption & decryption</p>
        </div>

        <div className="crypto-controls">
          <label>Algorithm</label>
          <select
            value={algorithm}
            onChange={(e) => {
              setAlgorithm(e.target.value);
              setAction("encrypt");
              setResult("");
              setError("");
              setKey("");
              setShowKey(false);
            }}
          >
            <option value="caesar">Caesar Cipher</option>
            <option value="aes">AES (256-bit)</option>
            <option value="des">DES (56-bit)</option>
            <option value="3des">3DES (Triple DES)</option>
            <option value="blowfish">Blowfish</option>
            <option value="rc4">RC4 (Stream Cipher)</option>
            <option value="chacha20">ChaCha20</option>
            <option value="rsa">RSA (2048-bit)</option>
          </select>

          {algorithm === "caesar" && (
            <div className="crypto-meta">
              Fixed Shift: <strong>{CAESAR_SHIFT}</strong>
            </div>
          )}
        </div>
      </div>

      {/* RSA Recommendation */}
      {algorithm === "rsa" && (
        <div className="crypto-recommendation">
          <strong>🔐 RSA Usage Recommendation</strong>
          <ul>
            <li>Generate keys on the receiver’s device</li>
            <li>Share only the public key</li>
            <li>Never share the private key</li>
          </ul>
        </div>
      )}

      {/* Workspace */}
      <div className="crypto-workspace">
        {/* Input */}
        <div className="crypto-panel">
          <label>Input Text</label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            disabled={algorithm === "rsa" && action === "generate"}
          />

          {(algorithm !== "caesar" &&
            !(algorithm === "rsa" && action === "generate")) && (
            <>
              <label>
                {algorithm === "rsa"
                  ? action === "decrypt"
                    ? "Private Key"
                    : "Public Key"
                  : "Passphrase"}
              </label>

              {algorithm === "rsa" ? (
                <textarea
                  className="crypto-key-area"
                  value={key}
                  onChange={(e) => setKey(e.target.value)}
                  rows={6}
                />
              ) : (
                <div className="password-wrapper">
                  <input
                    type={showKey ? "text" : "password"}
                    value={key}
                    onChange={(e) => setKey(e.target.value)}
                  />
                  <span
                    className="toggle-eye"
                    onClick={() => setShowKey(!showKey)}
                  >
                    {showKey ? "🙈" : "👁️"}
                  </span>
                </div>
              )}
            </>
          )}

          <label>Action</label>
          <select value={action} onChange={(e) => setAction(e.target.value)}>
            {algorithm === "rsa" ? (
              <>
                <option value="generate">Generate Keys</option>
                <option value="encrypt">Encrypt</option>
                <option value="decrypt">Decrypt</option>
              </>
            ) : (
              <>
                <option value="encrypt">Encrypt</option>
                <option value="decrypt">Decrypt</option>
              </>
            )}
          </select>

          <button onClick={handleSubmit} disabled={loading}>
            {loading ? "Processing..." : "Run"}
          </button>
        </div>

        {/* Output */}
        <div className="crypto-panel">
          <div className="crypto-output-header">
            <label>Output</label>
            <button onClick={handleCopy} disabled={!result}>
              {copied ? "Copied" : "Copy"}
            </button>
          </div>

          <pre className="crypto-output">
            {result || "Output will appear here"}
          </pre>

          {error && <div className="crypto-error">{error}</div>}
        </div>
      </div>
    </div>
  );
}

export default Crypto;