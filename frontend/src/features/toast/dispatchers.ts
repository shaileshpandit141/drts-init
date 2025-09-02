import { nanoid } from "@reduxjs/toolkit";
import { store } from "app/store";
import { addToast, resetToastState } from "./toastSlice";

export const triggerToast = (
  type: "success" | "error" | "info" | "warning",
  message: string,
  duration?: number
) => {
  const id = nanoid();
  store.dispatch(
    addToast({
      id,
      type,
      message,
      duration,
    })
  );
};

export const resetToast = (): void => {
  store.dispatch(resetToastState());
};
