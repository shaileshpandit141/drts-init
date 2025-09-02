import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../features/auth/hooks";

const PrivateRoute = () => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <Outlet /> : <Navigate to="/signin" replace />;
};

export default PrivateRoute;
