import { RootState } from "app/store";
import { useSelector } from "react-redux";

export const useToast = () => {
  return useSelector((state: RootState) => state.toast.toasts);
};
