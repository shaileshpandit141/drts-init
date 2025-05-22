import { InitialState, SuccessResponse, ErrorResponse } from "BaseAPITypes";

/**
 * Interface for Verify User Account initial state
 */
export interface VerifyUserAccountInitialState
  extends InitialState<{ detail: string } | null, { token?: string[] }> {}

/**
 * Interface for successful Verify User Account response
 */
export interface VerifyUserAccountSuccessResponse
  extends SuccessResponse<{ detail: string }> {}

export interface VerifyUserAccountErrorResponse
  extends ErrorResponse<{
    token?: string[];
  }> {}
