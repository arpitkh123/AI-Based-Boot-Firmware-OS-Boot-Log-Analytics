import { Outlet } from "react-router-dom";
import Navbar from "../components/layout/Navbar";

function MainLayout() {
  return (
    <div className="min-h-screen bg-base-200 flex flex-col">
      <Navbar />
      <main className="flex-1 p-6">
        <Outlet />
      </main>
    </div>
  );
}

export default MainLayout;