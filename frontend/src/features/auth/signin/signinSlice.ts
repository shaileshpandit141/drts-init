import { createSlice } from "@reduxjs/toolkit";
import {
  SigninInitialState,
  SigninErrorResponse,
  RefreshTokenErrorResponse,
} from "./signin.types";
import {
  signinAction,
  googleSigninAction,
  refreshTokenAction,
} from "./signinActions";

/**
 * Initial authentication state with tokens from localStorage
 */
const signinIntitlState: SigninInitialState = {
  status: "idle",
  status_code: null,
  message: null,
  data: {
    access_token: localStorage.getItem("access_token"),
    refresh_token: localStorage.getItem("refresh_token"),
  },
  errors: null,
  meta: null,
};

/**
 * Authentication slice definition with reducers and async thunks
 */
const signinSlice = createSlice({
  name: "signin",
  initialState: signinIntitlState,
  reducers: {
    // Reset auth state and clear stored tokens
    resetSigninState: (state) => {
      state.status = "idle";
      state.message = null;
      state.data = null;
      state.data = null;
      state.errors = null;
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    },
    resetSigninErrorsState: (state) => {
      state.status = "idle";
      state.message = null;
      state.errors = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Handle signin process states
      .addCase(signinAction.pending, (state) => {
        state.status = "loading";
      })
      .addCase(signinAction.fulfilled, (state, action) => {
        const { status, message, data, meta } = action.payload;
        state.status = status;
        state.message = message;
        state.data = data;
        state.meta = meta;
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);
      })
      .addCase(signinAction.rejected, (state, action) => {
        const { status, message, errors } =
          action.payload as SigninErrorResponse;
        state.status = status;
        state.message = message;
        state.errors = errors;
      })

      // Handle google signin process states
      .addCase(googleSigninAction.pending, (state) => {
        state.status = "loading";
      })
      .addCase(googleSigninAction.fulfilled, (state, action) => {
        const { status, message, data, meta } = action.payload;
        state.status = status;
        state.message = message;
        state.data = data;
        state.meta = meta;
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);
      })
      .addCase(googleSigninAction.rejected, (state, action) => {
        const { status, message, errors } =
          action.payload as SigninErrorResponse;
        state.status = status;
        state.message = message;
        state.errors = errors;
      })

      // Handle token refresh states
      .addCase(refreshTokenAction.pending, (state) => {
        state.status = "loading";
      })
      .addCase(refreshTokenAction.fulfilled, (state, action) => {
        const { status_code, message, data, meta } = action.payload;
        state.status = "succeeded";
        state.status_code = status_code;
        state.message = message;
        state.data = {
          access_token: data.access_token,
          refresh_token: state.data && state.data.refresh_token,
        };
        localStorage.setItem("access_token", data.access_token);
        state.meta = meta;
      })
      .addCase(refreshTokenAction.rejected, (state, action) => {
        const { message, errors, meta } =
          action.payload as RefreshTokenErrorResponse;
        state.status = "failed";
        state.message = message;
        state.meta = meta;
        state.errors = errors;
        state.data = {
          access_token: null,
          refresh_token: null,
        };
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
      });
  },
});

export const {
  reducer: signinReducer,
  actions: { resetSigninState, resetSigninErrorsState },
} = signinSlice;
