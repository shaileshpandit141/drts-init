import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { Toast, ToastState } from "./types";

const initialState: ToastState = {
  toasts: [],
};

const toastSlice = createSlice({
  name: "toast",
  initialState,
  reducers: {
    resetToastState: (state) => {
      Object.assign(state, initialState);
    },
    addToast: (state, action: PayloadAction<Toast>) => {
      state.toasts.push(action.payload);
    },
    removeToast: (state, action: PayloadAction<string>) => {
      state.toasts = state.toasts.filter(
        (toast) => toast.id !== action.payload
      );
    },
  },
});

export const { addToast, removeToast, resetToastState } = toastSlice.actions;
export default toastSlice.reducer;
