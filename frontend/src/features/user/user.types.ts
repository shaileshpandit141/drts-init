import { InitialState, SuccessResponse, ErrorResponse } from "BaseAPITypes";

/**
 * Interface representing core user data fields
 * Contains basic user information and authentication status
 */
export interface UserData {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  picture: string;
  is_verified: boolean;
  is_staff: boolean;
  is_superuser: boolean;
}

/**
 * Interface extending InitialState to handle UserData
 * Used for managing user state with nullable UserData
 */
export interface UserInitialState
  extends InitialState<UserData | null, {} | null> {}

/**
 * Interface extending SuccessResponse for UserData
 * Used for handling successful user data API responses
 */
export interface UserSuccessResponse extends SuccessResponse<UserData> {}

export interface UserErrorResponse extends ErrorResponse<{}> {}
