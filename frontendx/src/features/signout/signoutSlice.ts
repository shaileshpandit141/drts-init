import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { SignoutState, SignoutResponse } from "./types";

const initialState: SignoutState = {
  detail: "",
};

const signoutSlice = createSlice({
  name: "signout",
  initialState,
  reducers: {
    setSignoutState: (state, action: PayloadAction<SignoutResponse>) => {
      state.detail = action.payload.detail;
    },
  },
});

export const { setSignoutState } = signoutSlice.actions;
export default signoutSlice.reducer;
