import { useSelector, useDispatch } from "react-redux";
import type { RootState, AppDispatch } from "app/store";

export const useAuth = () => {
  return useSelector((state: RootState) => state.auth);
};

export const useAppDispatch = () => useDispatch<AppDispatch>();
