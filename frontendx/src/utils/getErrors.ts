import { SerializedError } from "@reduxjs/toolkit";
import { FetchBaseQueryError } from "@reduxjs/toolkit/query";

export interface Errors<ErrorResponse = Record<string, any>> {
  status: number;
  data: {
    detail?: string;
    non_field?: string[];
  } & ErrorResponse; // merge custom fields with default ones
}

// Type guard for FetchBaseQueryError
function isFetchBaseQueryError(error: any): error is FetchBaseQueryError {
  return (
    error && typeof error === "object" && "status" in error && "data" in error
  );
}

// Generic GetErrors function
export function GetErrors<ErrorResponse = Record<string, any>>(
  error: FetchBaseQueryError | SerializedError | undefined
): Errors<ErrorResponse> {
  if (isFetchBaseQueryError(error)) {
    return {
      status: error.status as number,
      data: error.data as Errors<ErrorResponse>["data"],
    };
  }

  // Handle SerializedError fallback
  if (error && "message" in error) {
    return {
      status: 0,
      data: { detail: error.message } as Errors<ErrorResponse>["data"],
    };
  }

  // Default empty error
  return {
    status: 0,
    data: {} as Errors<ErrorResponse>["data"],
  };
}
