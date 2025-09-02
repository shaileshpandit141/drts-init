import { RootState } from "app/store";
import { useSelector } from "react-redux";

export const useToastSelector = () => {
  return useSelector((state: RootState) => state.toast.toasts);
};
