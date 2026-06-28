import { createBrowserRouter, Navigate } from "react-router-dom";

// import Upload from "./pages/Upload/Upload";
import UploadPage from "./pages/Upload/Upload";
import Processing from "./pages/Processing/Processing";
import Analysis from "./pages/Analysis/Analysis";
import History from "./pages/History/History";
import Settings from "./pages/Settings/Settings";

import MainLayout from "./layouts/MainLayout";

const router = createBrowserRouter([
  {    
    path: "/",
    element: <Navigate to="/upload" replace />,
  },

//   {
//     path: "/upload",
//     element: <Upload />,
//   },

    {
        path: "/upload",
        element: <UploadPage />,
    },

  {
    element: <MainLayout />,
    children: [
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





// import { createBrowserRouter, Navigate } from "react-router-dom";

// import Upload from "./pages/Upload/Upload";
// import Processing from "./pages/Processing/Processing";
// import Analysis from "./pages/Analysis/Analysis";
// import History from "./pages/History/History";
// import Settings from "./pages/Settings/Settings";

// const router = createBrowserRouter([
//   {
//     path: "/",
//     element: <Navigate to="/upload" replace />,
//   },
//   {
//     path: "/upload",
//     element: <Upload />,
//   },
//   {
//     path: "/processing",
//     element: <Processing />,
//   },
//   {
//     path: "/analysis",
//     element: <Analysis />,
//   },
//   {
//     path: "/history",
//     element: <History />,
//   },
//   {
//     path: "/settings",
//     element: <Settings />,
//   },
// ]);

// export default router;