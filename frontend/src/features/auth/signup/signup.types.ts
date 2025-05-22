import { InitialState, SuccessResponse, ErrorResponse } from "BaseAPITypes";

export interface SignuResponseData {
  detail: string;
}

/**
 * Interface for signup initial state
 */
export interface SignupInitialState
  extends InitialState<
    { detail: string } | null,
    {
      email?: string[];
      password?: string[];
      confirm_password?: string[];
    }
  > {}

/**
 * Interface for successful signup response
 */
export interface SignupSuccessResponse
  extends SuccessResponse<{
    detail: string;
  }> {}

/**
 * Interface for failed signup response
 */
export interface SignupErrorResponse
  extends ErrorResponse<{
    email?: string[];
    password?: string[];
    confirm_password?: string[];
  }> {}
