export interface SignupRequest {
  email: string;
  password: string;
}

export interface SignupResponse {
  detail: string;
}

export interface SignupErrorResponse {
  email?: string[];
  password?: string[];
}
