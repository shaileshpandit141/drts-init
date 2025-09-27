import { useMemo, useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { SerializedError } from "@reduxjs/toolkit";
import { FetchBaseQueryError } from "@reduxjs/toolkit/query";

export interface Errors<CustomFields = Record<string, unknown>> {
  status: number;
  data: {
    detail?: string;
    non_field_errors?: string[];
  } & CustomFields;
}

interface UseApiErrorResult<CustomFields> {
  hasApiError: boolean;
  apiError: Errors<CustomFields>;
  resetError: () => void;
}

/** Type guard for FetchBaseQueryError */
function isFetchBaseQueryError(error: unknown): error is FetchBaseQueryError {
  return (
    !!error && typeof error === "object" && "status" in error && "data" in error
  );
}

// Default empty error to keep apiError non-null
const EMPTY_ERROR: Errors<any> = {
  status: 0,
  data: {},
};

/**
 * useApiError
 * - Normalizes API errors into a consistent format.
 * - Persists error state to avoid UI flicker during refetch.
 * - Resets automatically on route change (or manually with `resetError`).
 */
export function useApiError<CustomFields = Record<string, unknown>>(
  error: FetchBaseQueryError | SerializedError | undefined
): UseApiErrorResult<CustomFields> {
  const location = useLocation();
  const [storedError, setStoredError] = useState<Errors<CustomFields> | null>(
    null
  );

  const normalizedError = useMemo(() => {
    if (!error) return null;

    if (isFetchBaseQueryError(error)) {
      const data = (error.data || {}) as Errors<CustomFields>["data"];
      return {
        status: typeof error.status === "number" ? error.status : 0,
        data,
      };
    }

    if ("error" in error && typeof error.error === "string") {
      return {
        status: 0,
        data: { detail: error.error } as Errors<CustomFields>["data"],
      };
    }

    return {
      status: 0,
      data: {} as Errors<CustomFields>["data"],
    };
  }, [error]);

  // Update stored error only when we have a new one
  useEffect(() => {
    if (normalizedError) {
      setStoredError(normalizedError);
    }
  }, [normalizedError]);

  // Reset stored error on route change
  useEffect(() => {
    setStoredError(null);
  }, [location.pathname]);

  const resetError = () => setStoredError(null);

  const finalError = storedError ?? (EMPTY_ERROR as Errors<CustomFields>);

  return {
    hasApiError: !!storedError,
    apiError: finalError,
    resetError,
  };
}
