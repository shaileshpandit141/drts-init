import { InitialState, SuccessResponse, ErrorResponse } from "BaseAPITypes";

/** Initial state interface for signout feature */
export interface SignoutInitialState
  extends InitialState<
    { detail: string } | null,
    { refresh_token?: string[] } | null
  > {}

/** Success response interface for signout */
export interface SignoutSuccessResponse
  extends SuccessResponse<{ detail: string }> {}

/** Success response interface for signout */
export interface SignoutErrorResponse
  extends ErrorResponse<{ refresh_token?: string[] }> {}
