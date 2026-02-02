import ModuleCard from "../components/ModuleCard";
import "../styles/moduleSelect.css";

function ModuleSelect() {
  return (
    <div className="page">
      <h1 className="page-title">Select a Module</h1>
      <p className="page-subtitle">
        Choose one of the DeepTrace analysis modules
      </p>

      <div className="module-grid">
        <ModuleCard
          title="Cryptography"
          description="Encrypt and decrypt secure data"
          path="/crypto"
        />

        <ModuleCard
          title="Steganography"
          description="Hide data inside media"
          path="/stego"
        />

        <ModuleCard
          title="Watermarking"
          description="Embed ownership information"
          path="/watermark"
        />

        <ModuleCard
          title="Steganalysis"
          description="Detect hidden information"
          path="/analysis"
        />
      </div>
    </div>
  );
}

export default ModuleSelect;