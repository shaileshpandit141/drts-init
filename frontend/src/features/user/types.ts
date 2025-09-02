export interface UserState {
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  picture: string;
  is_varified: boolean;
  is_staff: boolean;
  is_superuser: boolean;
}

export interface UserResponse {
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  picture: string;
  is_varified: boolean;
  is_staff: boolean;
  is_superuser: boolean;
}

export interface UserErrorResponse {}
