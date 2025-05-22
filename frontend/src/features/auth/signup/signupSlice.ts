import { createSlice } from "@reduxjs/toolkit";
import { SignupInitialState } from "./signup.types";
import { signupAction } from "./signupAction";

/**
 * Initial state for signup slice
 * Contains status, message, data, errors and meta information
 */
const signupIntitlState: SignupInitialState = {
  status: "idle",
  status_code: null,
  message: null,
  data: null,
  errors: null,
  meta: null,
};

/**
 * Redux slice containing signup state logic and reducers
 */
const signupSlice = createSlice({
  name: "signup",
  initialState: signupIntitlState,
  reducers: {
    // Reset signup state to initial values
    resetSignupState: (state) => {
      Object.assign(state, signupIntitlState);
    },
  },
  extraReducers: (builder) => {
    builder
      // Handle signup async states
      .addCase(signupAction.pending, (state) => {
        state.status = "loading";
      })
      .addCase(signupAction.fulfilled, (state, action) => {
        Object.assign(state, action.payload);
        state.status = "succeeded";
      })
      .addCase(signupAction.rejected, (state, action) => {
        Object.assign(state, action.payload);
        state.status = "failed";
      });
  },
});

// Extract reducer and actions
export const {
  reducer: signupReducer,
  actions: { resetSignupState },
} = signupSlice;
