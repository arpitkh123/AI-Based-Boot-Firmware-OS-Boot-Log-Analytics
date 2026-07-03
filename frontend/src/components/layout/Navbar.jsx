import { NavLink, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const navLinkClass = ({ isActive }) =>
    isActive
      ? "btn btn-ghost btn-sm text-primary font-semibold"
      : "btn btn-ghost btn-sm text-base-content/70 hover:text-base-content";

  return (
    <div className="navbar bg-base-100 border-b border-base-300 px-4 min-h-[64px]">

      {/* ── Brand ── */}
      <div className="navbar-start">
        <div
          className="flex items-center gap-3 cursor-pointer select-none"
          onClick={() => navigate("/upload")}
          title="Go to Upload"
        >
          {/* CPU chip icon */}
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 32 32"
            fill="none"
            className="w-8 h-8 shrink-0"
          >
            <rect width="32" height="32" rx="6" fill="currentColor" className="text-primary" opacity="0.15" />
            <rect x="9" y="9" width="14" height="14" rx="2" stroke="currentColor" strokeWidth="1.5" className="text-primary" />
            <line x1="13" y1="9" x2="13" y2="23" stroke="currentColor" strokeWidth="0.75" opacity="0.5" className="text-primary" />
            <line x1="16" y1="9" x2="16" y2="23" stroke="currentColor" strokeWidth="0.75" opacity="0.5" className="text-primary" />
            <line x1="19" y1="9" x2="19" y2="23" stroke="currentColor" strokeWidth="0.75" opacity="0.5" className="text-primary" />
            <line x1="9" y1="13" x2="23" y2="13" stroke="currentColor" strokeWidth="0.75" opacity="0.5" className="text-primary" />
            <line x1="9" y1="16" x2="23" y2="16" stroke="currentColor" strokeWidth="0.75" opacity="0.5" className="text-primary" />
            <line x1="9" y1="19" x2="23" y2="19" stroke="currentColor" strokeWidth="0.75" opacity="0.5" className="text-primary" />
            <line x1="12" y1="6" x2="12" y2="9" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" className="text-primary" />
            <line x1="16" y1="6" x2="16" y2="9" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" className="text-primary" />
            <line x1="20" y1="6" x2="20" y2="9" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" className="text-primary" />
            <line x1="12" y1="23" x2="12" y2="26" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" className="text-primary" />
            <line x1="16" y1="23" x2="16" y2="26" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" className="text-primary" />
            <line x1="20" y1="23" x2="20" y2="26" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" className="text-primary" />
            <line x1="6" y1="12" x2="9" y2="12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" className="text-primary" />
            <line x1="6" y1="16" x2="9" y2="16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" className="text-primary" />
            <line x1="6" y1="20" x2="9" y2="20" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" className="text-primary" />
            <line x1="23" y1="12" x2="26" y2="12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" className="text-primary" />
            <line x1="23" y1="16" x2="26" y2="16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" className="text-primary" />
            <line x1="23" y1="20" x2="26" y2="20" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" className="text-primary" />
            <rect x="13" y="13" width="6" height="6" rx="1" fill="currentColor" className="text-primary" />
          </svg>

          <div className="flex flex-col leading-tight">
            <span className="text-sm font-bold text-base-content tracking-wide">
              Boot Log Analytics
            </span>
            <span className="text-[10px] text-base-content/40 font-mono tracking-widest uppercase">
              AI Firmware Diagnostics
            </span>
          </div>
        </div>
      </div>

      {/* ── Nav Links (center) ── */}
      <div className="navbar-center hidden md:flex gap-1">
        <NavLink to="/analysis" className={navLinkClass}>
          Analysis
        </NavLink>
        <NavLink to="/history" className={navLinkClass}>
          History
        </NavLink>
        <NavLink to="/settings" className={navLinkClass}>
          Settings
        </NavLink>
      </div>

      {/* ── Right side ── */}
      <div className="navbar-end gap-3">
        <div className="badge badge-outline badge-sm font-mono text-base-content/50">
          v1.0
        </div>
        <button
          className="btn btn-primary btn-sm"
          onClick={() => navigate("/upload")}
        >
          New Analysis
        </button>
      </div>

    </div>
  );
}

export default Navbar;