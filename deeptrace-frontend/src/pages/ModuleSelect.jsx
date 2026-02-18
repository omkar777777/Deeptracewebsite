import ModuleCard from "../components/ModuleCard";
import "../styles/moduleSelect.css";

function ModuleSelect() {
  return (
    <div className="page">
      <h1 className="page-title">Choose an Analysis Module</h1>
      <p className="page-subtitle">
        Select a module to analyze, protect, or verify digital media using secure and intelligent techniques.
      </p>

      <div className="module-grid">
        <ModuleCard
          title="Cryptography"
          description="Encrypt and decrypt secure data"
          path="/crypto"
          icon={
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
          }
        />

        <ModuleCard
          title="Steganography"
          description="Hide data inside media"
          path="/stego"
          icon={
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <circle cx="12" cy="14" r="2"></circle>
              <rect x="10" y="13" width="4" height="2" fill="currentColor" fillOpacity="0.2" stroke="none" />
            </svg>
          }
        />

        <ModuleCard
          title="Digital Watermarking"
          description="Embed ownership information"
          path="/watermark"
          icon={
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path>
            </svg>
          }
        />

        <ModuleCard
          title="Steganalysis"
          description="Detect hidden information"
          path="/analysis"
          icon={
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
          }
        />
      </div>

      <p style={{
        textAlign: "center",
        marginTop: "40px",
        color: "var(--text-secondary)",
        fontSize: "0.95rem",
        fontStyle: "italic"
      }}>
        Each module supports file upload, processing, and result analysis.
      </p>
    </div>
  );
}

export default ModuleSelect;