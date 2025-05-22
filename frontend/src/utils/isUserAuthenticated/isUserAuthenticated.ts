const decodeBase64Url = (str: string): any => {
  str = str.replace(/-/g, "+").replace(/_/g, "/");
  const pad = str.length % 4;
  if (pad) {
    str += "=".repeat(4 - pad);
  }
  try {
    return JSON.parse(atob(str));
  } catch {
    return null;
  }
};

const getRefreshToken = (): string | null => {
  try {
    return localStorage.getItem("refresh_token");
  } catch (error) {
    console.error("Error accessing localStorage:", error);
    return null;
  }
};

export const isUserAuthenticated = (): boolean => {
  const token = getRefreshToken();
  if (!token) return false;

  const parts = token.split(".");
  if (parts.length !== 3) return false;

  const payload = decodeBase64Url(parts[1]);
  if (!payload?.exp) return false;

  const expirationDate = payload.exp * 1000;
  return Date.now() < expirationDate;
};
