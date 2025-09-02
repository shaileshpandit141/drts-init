import { configureStore } from "@reduxjs/toolkit";
import authReducer from "features/auth/authSlice";
import { authApi } from "features/auth/authApi";
import { toastReducer } from "features/toast";

export const store = configureStore({
  reducer: {
    auth: authReducer,
    [authApi.reducerPath]: authApi.reducer,
    toast: toastReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(authApi.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
