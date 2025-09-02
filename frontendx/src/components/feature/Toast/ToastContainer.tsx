import React from "react";
import "./ToastContainer.css";
import Toast from "./index";
import { useToastSelector } from "features/toast";

const ToastContainer: React.FC = () => {
  const toasts = useToastSelector();

  return (
    <div className="toast-container">
      <div className="toasts">
        {[...toasts].reverse().map((toast) => (
          <Toast
            key={toast.id}
            id={toast.id}
            type={toast.type}
            message={toast.message}
            duration={toast.duration}
          />
        ))}
      </div>
    </div>
  );
};

export default ToastContainer;
