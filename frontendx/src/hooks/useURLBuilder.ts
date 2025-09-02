import { useMemo } from "react";

interface URLBuilderOptions {
  baseUrl?: string;
  path?: string;
  queryParams?: Record<string, any>;
}

export const useURLBuilder = ({
  baseUrl,
  path = "",
  queryParams = {},
}: URLBuilderOptions = {}) => {
  const builtUrl = useMemo(() => {
    // Determine the base URL (default to the current origin)
    const resolvedBaseUrl = baseUrl || window.location.origin;

    // If no path and no query params, return only the base URL
    if (!path && Object.keys(queryParams).length === 0) {
      return resolvedBaseUrl;
    }

    // Remove leading slashes from path
    let fullUrl = `${resolvedBaseUrl}/${path.replace(/^\/+/, "")}`;

    // Build query string
    const query = new URLSearchParams();
    Object.entries(queryParams).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        query.append(key, String(value));
      }
    });

    if (query.toString()) {
      fullUrl += `?${query.toString()}`;
    }

    return fullUrl;
  }, [path, queryParams, baseUrl]);

  return builtUrl;
};
