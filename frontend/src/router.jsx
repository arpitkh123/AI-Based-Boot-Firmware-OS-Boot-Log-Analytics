import { createBrowserRouter, Navigate } from "react-router-dom";

import UploadPage from "./pages/Upload/Upload";
import Processing from "./pages/Processing/Processing";
import Analysis from "./pages/Analysis/Analysis";
import History from "./pages/History/History";
import Settings from "./pages/Settings/Settings";

import MainLayout from "./layouts/MainLayout";

const router = createBrowserRouter([
  {
    element: <MainLayout />,
    children: [
      {
        path: "/",
        element: <Navigate to="/upload" replace />,
      },
      {
        path: "/upload",
        element: <UploadPage />,
      },
      {
        path: "/processing",
        element: <Processing />,
      },
      {
        path: "/analysis",
        element: <Analysis />,
      },
      {
        path: "/history",
        element: <History />,
      },
      {
        path: "/settings",
        element: <Settings />,
      },
    ],
  },
]);

export default router;