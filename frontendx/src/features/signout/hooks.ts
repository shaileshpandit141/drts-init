import { useSelector, useDispatch } from "react-redux";
import type { RootState, AppDispatch } from "app/store";

export const useSignout = () => {
  return useSelector((state: RootState) => state.signout);
};

export const useAppDispatch = () => useDispatch<AppDispatch>();
