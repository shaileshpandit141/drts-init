import React, { useEffect, useState } from "react";
import "./Toast.css";
import { useDispatch } from "react-redux";
import { removeToast } from "features/toast/toastSlice";
import { CheckCheck, Info, CircleAlert, Ban, X } from "lucide-react";

interface ToastProps {
  id: string;
  type: "success" | "info" | "warning" | "error";
  message: string;
  duration?: number;
}

const Toast: React.FC<ToastProps> = ({
  id,
  type,
  message,
  duration = 5000,
}) => {
  const dispatch = useDispatch();
  const [isRemoving, setIsRemoving] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsRemoving(true);
      setTimeout(() => {
        dispatch(removeToast(id));
      }, 300);
    }, duration);

    return () => clearTimeout(timer);
  }, [dispatch, id, duration]);

  const handleClose = () => {
    setIsRemoving(true);
    setTimeout(() => {
      dispatch(removeToast(id));
    }, 300);
  };

  const randerIcon = () => {
    if (type === "success") {
      return <CheckCheck />
    } else if (type === "info") {
      return <Info />
    } else if (type === "warning") {
      return <CircleAlert />
    } else {
      return <Ban />
    }
  }

  return (
    <div className={`toast toast-${type} ${isRemoving ? "toast-removed" : ""}`}>
      <section className="toast-icon-container">
        <div className="icon-container">
          {randerIcon()}
        </div>
      </section>
      <section className="message-container">
        <p className="error-message">{message}</p>
      </section>
      <section className="button-container">
        <button className="toast-close-button" onClick={handleClose}>
          <div className="icon-container">
            <X />
          </div>
        </button>
      </section>
    </div>
  );
};

export default Toast;
