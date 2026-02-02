import { useNavigate } from "react-router-dom";
import "../styles/home.css";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home">
      <div className="home-inner">
        <h1 className="home-title">DeepTrace</h1>

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