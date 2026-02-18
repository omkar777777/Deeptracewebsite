import { Link } from "react-router-dom";

function ModuleCard({ title, description, path, icon }) {
  return (
    <Link to={path} className="module-card">
      <div className="module-icon" style={{ marginBottom: "15px", color: "var(--accent)" }}>
        {icon}
      </div>
      <h2>{title}</h2>
      <p>{description}</p>

    </Link>
  );
}

export default ModuleCard;