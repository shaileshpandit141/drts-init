import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../features/auth/hooks";

const PublicRoute = () => {
  const { isAuthenticated } = useAuth();
  return !isAuthenticated ? <Outlet /> : <Navigate to="/dashboard" replace />;
};

export default PublicRoute;
