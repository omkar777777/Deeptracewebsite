import "../../styles/steganalysis.css";

function RiskMeter({ score }) {
  if (score === undefined || score === null) return null;

  const getRiskColor = () => {
    if (score <= 30) return "#4CAF50"; // Green
    if (score <= 60) return "#FFC107"; // Yellow
    return "#F44336"; // Red
  };

  const getRiskLabel = () => {
    if (score <= 30) return "Clean";
    if (score <= 60) return "Suspicious";
    return "High Risk";
  };

  const color = getRiskColor();
  const label = getRiskLabel();

  return (
    <div className="risk-container">
      <h2>Risk Assessment</h2>

      {/* Progress Bar */}
      <div className="progress-bar-bg">
        <div
          className="progress-bar-fill"
          style={{
            width: `${score}%`,
            backgroundColor: color,
          }}
        />
      </div>

      {/* Score & Label */}
      <h3 className="risk-label" style={{ color }}>
        {score}% — {label}
      </h3>
    </div>
  );
}

export default RiskMeter;