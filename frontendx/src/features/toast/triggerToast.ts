import { nanoid } from "@reduxjs/toolkit";
import { store } from "app/store";
import { addToast } from "features/toast";

// Triggers a toast notification with the specified parameters
export const triggerToast = (
  type: "success" | "error" | "info" | "warning",
  message: string,
  duration?: number,
) => {
  const id = nanoid();
  store.dispatch(
    addToast({
      id,
      type,
      message,
      duration,
    }),
  );
};
