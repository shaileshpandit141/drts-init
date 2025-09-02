import { configureStore } from "@reduxjs/toolkit";
import toastReducer from "features/toast/toastSlice";
import { authApi } from "features/auth/authApi";
import authReducer from "features/auth/authSlice";
import { signoutApi } from "features/signout/signoutApi";
import signoutReducer from "features/signout/signoutSlice";

export const store = configureStore({
  reducer: {
    toast: toastReducer,
    auth: authReducer,
    [authApi.reducerPath]: authApi.reducer,
    signout: signoutReducer,
    [signoutApi.reducerPath]: signoutApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(authApi.middleware, signoutApi.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
