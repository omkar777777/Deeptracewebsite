import { useNavigate } from "react-router-dom";
import "../styles/home.css";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home">
      <div className="home-inner">
        <h1 className="home-title">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            style={{ marginBottom: "-8px", marginRight: "12px", color: "var(--accent)" }}
          >
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
          </svg>
          DeepTrace
        </h1>

        <p className="home-subtitle">
          DeepTrace is a unified research platform designed to study, apply,
          and analyze data-hiding and information-security techniques.
        </p>

        <p className="home-intro">
          It integrates cryptography, steganography, watermarking, and
          steganalysis into a single environment, enabling structured
          exploration of both protection and detection mechanisms.
        </p>

        <button
          className="home-cta"
          onClick={() => navigate("/modules")}
        >
          Enter Modules →
        </button>
      </div>
    </div>
  );
}

export default Home;