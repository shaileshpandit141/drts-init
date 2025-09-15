import { BrowserRouter, Routes, Route } from "react-router-dom";
import PrivateRoute from "routes/PrivateRoute";
import PublicRoute from "routes/PublicRoute";
import RootLayout from "layouts/RootLayout";
import AuthLayout from "layouts/AuthLayout";
import MainLayout from "layouts/MainLayout";
import Signin from "pages/Signin";
import Signup from "pages/Signup";
import Home from "pages/Home";

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
              <Route path="/signup" element={<Signup />} />
            </Route>
            {/* All public routes with main layout goes here. */}
            <Route element={<MainLayout />}>
              <Route index element={<Home />} />
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
