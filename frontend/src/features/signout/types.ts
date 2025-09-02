export interface SignoutState {
  detail: string;
}

export interface SignoutRequest {
  refresh_token: string;
}

export interface SignoutResponse {
  detail: string;
}

export interface SignoutErrorResponse {
  refresh_token: string[];
}
