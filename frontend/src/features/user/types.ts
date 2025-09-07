export interface UserState {
  email: string;
  first_name: string;
  last_name: string;
  picture: string;
  is_varified: boolean;
  is_staff: boolean;
  is_superuser: boolean;
}

export interface UserResponse {
  email: string;
  first_name: string;
  last_name: string;
  picture: string;
  is_varified: boolean;
  is_staff: boolean;
  is_superuser: boolean;
}
