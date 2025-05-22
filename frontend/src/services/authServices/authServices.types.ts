// Credentials for user sign in
export interface SigninCredentials {
  email: string;
  password: string;
}

// Credentials for user google sign in
export interface GoogleSigninCredentials {
  token: string;
}

// Credentials for new user registration
export interface SignupCredentials {
  email: string;
  password: string;
  confirm_password: string;
  verification_uri: string;
}

// Credentials for user sign out
export interface SignoutCredentials {
  refresh_token: string;
}

// Credentials for refreshing authentication token
export interface RefreshTokenCredentials {
  refresh_token: string;
}

// Credentials for verifying user account
export interface VerifyUserAccountCredentials {
  token: string;
}
