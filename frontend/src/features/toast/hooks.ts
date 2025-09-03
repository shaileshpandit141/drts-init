import { useDispatch, useSelector } from "react-redux";
import { nanoid } from "@reduxjs/toolkit";
import { RootState } from "app/store";
import { addToast, resetToastState } from "./toastSlice";
import { ToastType } from "./types";

export const useToast = () => {
  const dispatch = useDispatch();
  const toasts = useSelector((state: RootState) => state.toast.toasts);

  const triggerToast = (
    type: ToastType,
    message: string,
    duration?: number
  ): void => {
    if (!message.trim()) {
      console.warn("Toast message cannot be empty");
      return;
    }
    if (duration && duration <= 0) {
      console.warn("Toast duration must be positive");
      return;
    }

    const id = nanoid();
    dispatch(
      addToast({
        id,
        type,
        message,
        duration,
      })
    );
  };

  const resetToast = (): void => {
    dispatch(resetToastState());
  };

  return {
    toasts,
    triggerToast,
    resetToast,
  };
};
