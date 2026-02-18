import "../../styles/steganalysis.css";

function ScoreBreakdown({ details }) {
  if (!details) return null;

  const scoreItems = [
    { label: "LSB Analysis", value: details.lsb_score },
    { label: "Entropy Analysis", value: details.entropy_score },
    { label: "Histogram Analysis", value: details.histogram_score },
    { label: "Correlation Analysis", value: details.correlation_score },
    { label: "Chi-Square Analysis", value: details.chi_square_score },
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
            {item.value ?? 0} / 25
          </span>
        </div>
      ))}
    </div>
  );
}

export default ScoreBreakdown;