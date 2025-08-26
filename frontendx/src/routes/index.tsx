import { BrowserRouter, Routes, Route } from "react-router-dom";
import PrivateRoute from "routes/PrivateRoute";
import PublicRoute from "routes/PublicRoute";
import Signin from "pages/signin/Signin";
import RootLayout from "layouts/RootLayout";
import AuthLayout from "layouts/AuthLayout";
import MainLayout from "layouts/MainLayout";

function RootRoutes() {
  return (
    <BrowserRouter
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      }}
    >
      <Routes>
        <Route element={<RootLayout />}>
          {/* All public routes goes here. */}
          <Route element={<PublicRoute />}>
            {/* All public routes with auth layout goes here. */}
            <Route element={<AuthLayout />}>
              <Route path="/signin" element={<Signin />} />
            </Route>
            {/* All public routes with main layout goes here. */}
            <Route element={<MainLayout />}>
              <Route index element={<h2>Home</h2>} />
            </Route>
          </Route>
          {/* All private routes goes here. */}
          <Route element={<PrivateRoute />}>
            {/* All private routes with auth layout goes here. */}
            <Route element={<AuthLayout />}></Route>
            {/* All private routes with main layout goes here. */}
            <Route element={<MainLayout />}>
              <Route path="/dashboard" element={<h3>Dashboard</h3>} />
            </Route>
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default RootRoutes;
