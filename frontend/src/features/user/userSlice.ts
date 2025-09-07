import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { UserState, UserResponse } from "./types";

const initialState: UserState = {
  email: "",
  first_name: "",
  last_name: "",
  picture: "",
  is_varified: false,
  is_staff: false,
  is_superuser: false,
};

export const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    setUserState: (state, action: PayloadAction<UserResponse>) => {
      Object.assign(state, action.payload)
    },
  },
});

export const { setUserState } = userSlice.actions;

