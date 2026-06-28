import { Outlet } from "react-router-dom";
import Navbar from "../components/layout/Navbar";

function MainLayout() {
  return (
    <>
      <Navbar />

      <main
        style={{
          padding: "24px",
        }}
      >
        <Outlet />
      </main>
    </>
  );
}

export default MainLayout;