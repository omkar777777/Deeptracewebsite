function About() {
    return (
        <div className="page fade-in">
            <h1 className="page-title">About DeepTrace</h1>
            <p className="page-subtitle">
                Understanding the core technologies behind data security and concealment.
            </p>

            <div style={{ display: "grid", gap: "30px", marginTop: "30px" }}>

                {/* Cryptography */}
                <div className="card">
                    <h2 style={{ color: "var(--accent)", marginBottom: "10px" }}>Cryptography</h2>
                    <p style={{ lineHeight: "1.6", color: "var(--text-secondary)" }}>
                        Cryptography is the practice of securing communication from adversarial behavior.
                        It involves converting readable information (plaintext) into unintelligible text (ciphertext)
                        using mathematical algorithms. DeepTrace supports various symmetric (AES, DES) and
                        asymmetric (RSA) algorithms to ensure data confidentiality and integrity.
                    </p>
                </div>

                {/* Steganography */}
                <div className="card">
                    <h2 style={{ color: "var(--accent)", marginBottom: "10px" }}>Steganography</h2>
                    <p style={{ lineHeight: "1.6", color: "var(--text-secondary)" }}>
                        Derived from Greek words meaning "covered writing," Steganography is the technique of
                        hiding secret data within an ordinary, non-secret file or message in order to avoid detection.
                        Unlike cryptography, which scrambles the message, steganography hides the existence of the message entirely,
                        often embedding it into images (LSB), audio, or other media formats.
                    </p>
                </div>

                {/* Digital Watermarking */}
                <div className="card">
                    <h2 style={{ color: "var(--accent)", marginBottom: "10px" }}>Digital Watermarking</h2>
                    <p style={{ lineHeight: "1.6", color: "var(--text-secondary)" }}>
                        Digital watermarking involves embedding a marker covertly in a noise-tolerant signal such as an
                        audio, video or image data. It is typically used to identify ownership of the copyright of such signal.
                        DeepTrace offers both visible watermarks (overlays) and invisible watermarks (LSB) to prove authenticity
                        and track digital assets.
                    </p>
                </div>

                {/* Steganalysis */}
                <div className="card">
                    <h2 style={{ color: "var(--accent)", marginBottom: "10px" }}>Steganalysis</h2>
                    <p style={{ lineHeight: "1.6", color: "var(--text-secondary)" }}>
                        Steganalysis is the study of detecting messages hidden using steganography; this is analogous
                        to cryptanalysis applied to cryptography. The goal is to identify purely suspicious packages
                        that may contain hidden payloads. It employs statistical analysis and pattern recognition
                        to detect anomalies in media files that suggest unauthorized data embedding.
                    </p>
                </div>

            </div>
        </div>
    );
}

export default About;
