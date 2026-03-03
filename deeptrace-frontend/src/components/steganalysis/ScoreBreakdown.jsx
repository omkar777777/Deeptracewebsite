import "../../styles/steganalysis.css";

function ScoreBreakdown({ details }) {
  if (!details) return null;

  const scoreItems = [
    { label: "LSB Anomaly", value: `${details.lsb_anomaly_score ?? 0}%` },
    { label: "Entropy Deviation", value: `${details.entropy_deviation_score ?? 0}%` },
    { label: "Extraction Success", value: details.extraction_success ? "Yes" : "No" },
    { label: "Content Validity", value: details.content_validity ? "Valid" : "None" }
  ];

  return (
    <div className="score-container">
      <h2>Score Breakdown</h2>

      {scoreItems.map((item, index) => (
        <div key={index} className="score-card">
          <span className="score-label">
            {item.label}
          </span>
          <span className="score-value">
            {item.value}
          </span>
        </div>
      ))}
    </div>
  );
}

export default ScoreBreakdown;