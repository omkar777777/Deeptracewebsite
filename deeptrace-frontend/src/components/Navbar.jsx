import { Link, useLocation, useNavigate } from "react-router-dom";

function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();

  const isHome = location.pathname === "/";

  const isActive = (path) =>
    location.pathname === path ? "nav-link active" : "nav-link";

  return (
    <nav className="navbar">
      <div className="nav-inner">
        <div className="nav-left">
          {!isHome && (
            <button
              className="nav-back-btn"
              onClick={() => navigate(-1)}
              aria-label="Go back"
            >
              ←
            </button>
          )}

          <span className="nav-brand">DeepTrace</span>
        </div>

        <div className="nav-links">
          <Link to="/" className={isActive("/")}>Home</Link>
          <Link to="/modules" className={isActive("/modules")}>Modules</Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;