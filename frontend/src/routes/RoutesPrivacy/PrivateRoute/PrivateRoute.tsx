import { useEffect, useState } from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useSigninUserSelector, resetSigninUser } from "features/auth/signin";
import { useJWTDecoder } from "hooks/useJWTDecoder";

const PrivateRoute = (): JSX.Element => {
  const { data } = useSigninUserSelector();
  const refreshToken = data?.refresh_token || "";
  const { isExpired } = useJWTDecoder(refreshToken);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(true);
  const location = useLocation();

  useEffect(() => {
    if (!refreshToken || isExpired) {
      resetSigninUser();
      setIsAuthenticated(false);
    } else {
      setIsAuthenticated(true);
    }
  }, [refreshToken, isExpired]);

  return isAuthenticated ? (
    <Outlet />
  ) : (
    <Navigate to={`/sign-in?redirect_to=${location.pathname}`} replace />
  );
};

export default PrivateRoute;
