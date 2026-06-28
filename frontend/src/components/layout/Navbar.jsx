function Navbar() {
  return (
    <nav
      style={{
        height: "70px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 24px",
        borderBottom: "1px solid #ddd",
      }}
    >
      <h2>AI Boot Log Analytics</h2>

      <span>v1.0</span>
    </nav>
  );
}

export default Navbar;