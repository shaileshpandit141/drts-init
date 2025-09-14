export interface AuthState {
  access_token: string | null;
  refresh_token: string | null;
  isAuthenticated: boolean;
}

export interface SigninRequest {
  email: string;
  password: string;
}

export interface SigninResponse {
  access_token: string;
  refresh_token: string;
}

export interface SigninErrorResponse {
  email: string[];
  password: string[];
}
