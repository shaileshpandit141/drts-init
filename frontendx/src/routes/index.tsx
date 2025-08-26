import { BrowserRouter, Routes, Route } from "react-router-dom";
import PrivateRoute from "routes/PrivateRoute";
import PublicRoute from "routes/PublicRoute";
import Signin from "pages/signin/Signin";
import RootLayout from "layouts/RootLayout";

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
          <Route index element={<h3>Home Page</h3>} />

          <Route element={<PublicRoute />}>
            <Route path="/signin" element={<Signin />} />
          </Route>

          <Route element={<PrivateRoute />}>
            <Route path="/dashboard" element={<h3>Dashboard</h3>} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default RootRoutes;
