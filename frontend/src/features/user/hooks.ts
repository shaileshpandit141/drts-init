import { useSelector } from "react-redux";
import type { RootState } from "app/store";

export const useUser = () => {
  return useSelector((state: RootState) => state.user);
};
