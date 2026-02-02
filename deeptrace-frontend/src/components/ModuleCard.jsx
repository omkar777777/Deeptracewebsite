import { Link } from "react-router-dom";

function ModuleCard({ title, description, path }) {
  return (
    <div className="module-card">
      <h2>{title}</h2>
      <p>{description}</p>

      <Link to={path} className="module-link">
        Open →
      </Link>
    </div>
  );
}

export default ModuleCard;