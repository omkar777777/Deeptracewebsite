import ModuleCard from "../components/ModuleCard";
import "../styles/moduleSelect.css";

function WatermarkSelect() {
    return (
        <div className="page fade-in">
            <h1 className="page-title">Digital Watermarking</h1>
            <p className="page-subtitle">
                Choose an operation
            </p>

            <div className="module-grid">
                <ModuleCard
                    title="Embed Watermark"
                    description="Secure your images with visible or invisible watermarks."
                    path="/watermark/embed"
                    icon={
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path>
                            <path d="M12 12v6"></path>
                            <path d="M9 15l3 3 3-3"></path>
                        </svg>
                    }
                />

                <ModuleCard
                    title="Extract Watermark"
                    description="Extract hidden data from watermarked images using your key."
                    path="/watermark/recover"
                    icon={
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path>
                            <circle cx="12" cy="14" r="3"></circle>
                            <path d="M14.5 16.5L17 19"></path>
                        </svg>
                    }
                />
            </div>
        </div>
    );
}

export default WatermarkSelect;
