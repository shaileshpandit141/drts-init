import { CatchAxiosError, ErrorResponse, Errors } from "BaseAPITypes";

export const formatCatchAxiosError = <T = Record<string, any>>(
  error: CatchAxiosError,
): ErrorResponse<T> => {
  let errorResponse: ErrorResponse<T>;

  if (error.response) {
    errorResponse = error.response.data as ErrorResponse<T>;
  } else {
    errorResponse = {
      status: "failed",
      status_code: null,
      message: error.message ?? "An unknown error occurred",
      data: null,
      errors: {
        detail: error.message ?? "An unknown error occurred",
      } as Errors & T,
      meta: null,
    };
  }

  return errorResponse;
};
