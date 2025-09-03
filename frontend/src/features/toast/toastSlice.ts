import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { Toast, ToastState } from "./types";

const initialState: ToastState = {
  toasts: [],
};

export const toastSlice = createSlice({
  name: "toast",
  initialState,
  reducers: {
    addToast: (state, action: PayloadAction<Toast>) => {
      const { message, type } = action.payload;

      // check if a toast with the same message and type already exists
      const exists = state.toasts.some(
        (toast) => toast.message === message && toast.type === type
      );

      if (!exists) {
        state.toasts.push(action.payload);
      }
    },
    removeToast: (state, action: PayloadAction<string>) => {
      state.toasts = state.toasts.filter(
        (toast) => toast.id !== action.payload
      );
    },
    resetToastState: (state) => {
      Object.assign(state, initialState);
    },
  },
});

export const { addToast, removeToast, resetToastState } = toastSlice.actions;
