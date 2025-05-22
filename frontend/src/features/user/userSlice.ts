import { createSlice } from "@reduxjs/toolkit";
import { UserInitialState } from "./user.types";
import { userAction } from "./userAction";

/**
 * # Initial state for user slice
 * Contains status, message, data, errors and meta information
 */
const userInitialState: UserInitialState = {
  status: "idle",
  status_code: null,
  message: null,
  data: null,
  errors: null,
  meta: null,
};

/**
 * Redux slice containing user state logic and reducers
 */
const userSlice = createSlice({
  name: "user",
  initialState: userInitialState,
  reducers: {
    resetUserState: (state): void => {
      Object.assign(state, userInitialState);
    },
  },
  extraReducers: (builder) => {
    builder
      // Handle user async states
      .addCase(userAction.pending, (state) => {
        state.status = "loading";
      })
      .addCase(userAction.fulfilled, (state, action) => {
        Object.assign(state, action.payload);
        state.status = "succeeded";
      })
      .addCase(userAction.rejected, (state, action) => {
        Object.assign(state, action.payload);
        state.status = "failed";
      });
  },
});

// Export user slice actions
export const {
  reducer: userReducer,
  actions: { resetUserState },
} = userSlice;
