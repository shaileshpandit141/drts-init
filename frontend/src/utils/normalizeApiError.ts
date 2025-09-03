import { SerializedError } from "@reduxjs/toolkit";
import { FetchBaseQueryError } from "@reduxjs/toolkit/query";

// Standardized error interface
export interface Errors<CustomFields = Record<string, any>> {
  status: number;
  data: {
    detail?: string;
    non_field_errors?: string[]; // common backend field for general errors
  } & CustomFields; // merge with any backend-specific fields
}

// Type guard to check FetchBaseQueryError
function isFetchBaseQueryError(error: any): error is FetchBaseQueryError {
  return (
    error && typeof error === "object" && "status" in error && "data" in error
  );
}

/**
 * Normalize RTK Query or Redux Toolkit error.
 * Returns `undefined` if no error (success).
 * @param error - FetchBaseQueryError | SerializedError | undefined
 */
export function normalizeApiError<CustomFields = Record<string, any>>(
  error: FetchBaseQueryError | SerializedError | undefined
): Errors<CustomFields> | undefined {
  if (!error) return undefined; // No error => success

  // RTK Query FetchBaseQueryError
  if (isFetchBaseQueryError(error)) {
    const data = error.data as Errors<CustomFields>["data"];
    return {
      status: typeof error.status === "number" ? error.status : 0,
      data: data || ({} as Errors<CustomFields>["data"]),
    };
  }

  // Serialized Redux error
  if ("error" in error && typeof error.error === "string") {
    return {
      status: 0,
      data: { detail: error.error } as Errors<CustomFields>["data"],
    };
  }

  // Unknown error, fallback
  return {
    status: 0,
    data: {} as Errors<CustomFields>["data"],
  };
}
