// Interface representing a single toast notification
export interface Toast {
  id: string;
  type: "success" | "error" | "info" | "warning";
  message: string;
  duration?: number;
}

// Interface representing the state of all toast notifications
export interface ToastState {
  toasts: Toast[];
}
