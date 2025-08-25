import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AuthState, SigninResponse } from "./types";

const storedAuth = localStorage.getItem("auth");
const initialState: AuthState = storedAuth
  ? JSON.parse(storedAuth)
  : {
      access_token: null,
      refresh_token: null,
      isAuthenticated: false,
    };

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setCredentials: (state, action: PayloadAction<SigninResponse>) => {
      state.access_token = action.payload.access_token;
      state.refresh_token = action.payload.refresh_token;
      state.isAuthenticated = true;
      localStorage.setItem("auth", JSON.stringify(state));
    },
    signout: (state) => {
      state.access_token = null;
      state.refresh_token = null;
      state.isAuthenticated = false;
      localStorage.removeItem("auth");
    },
  },
});

export const { setCredentials, signout } = authSlice.actions;
export default authSlice.reducer;
