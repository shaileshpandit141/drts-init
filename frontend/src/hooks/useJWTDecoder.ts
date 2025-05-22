import { useMemo } from "react";

export interface JWTHeader {
  alg: string;
  typ: string;
  [key: string]: any;
}

export interface JWTPayload {
  exp?: number;
  iat?: number;
  [key: string]: any;
}

export interface DecodedJWT {
  header: JWTHeader;
  payload: JWTPayload;
  signature: string;
}

function decodeBase64Url(str: string): any {
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
}

export const useJWTDecoder = (token: string | null) => {
  const decoded: DecodedJWT | null = useMemo(() => {
    if (!token) return null;

    try {
      const [header, payload, signature] = token.split(".");
      if (!header || !payload || !signature) return null;

      const decodedHeader: JWTHeader = decodeBase64Url(header);
      const decodedPayload: JWTPayload = decodeBase64Url(payload);

      if (!decodedHeader || !decodedPayload) return null;

      return {
        header: decodedHeader,
        payload: decodedPayload,
        signature,
      };
    } catch (error) {
      console.error("Invalid JWT token:", error);
      return null;
    }
  }, [token]);

  const isExpired: boolean = useMemo(() => {
    if (!decoded?.payload?.exp) return true;

    const expirationDate = decoded.payload.exp * 1000;
    return Date.now() > expirationDate;
  }, [decoded]);

  return {
    decoded,
    isExpired,
  };
};
