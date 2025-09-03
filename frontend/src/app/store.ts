import { configureStore } from "@reduxjs/toolkit";
import { authenticatedApi } from "./authenticatedApi";
import { publicApi } from "./publicApi";
import { toastSlice } from "features/toast/toastSlice";
import { authSlice } from "features/auth/authSlice";
import { signoutSlice } from "features/signout/signoutSlice";
import { userSlice } from "features/user/userSlice";

export const store = configureStore({
  reducer: {
    toast: toastSlice.reducer,
    auth: authSlice.reducer,
    signout: signoutSlice.reducer,
    user: userSlice.reducer,
    [authenticatedApi.reducerPath]: authenticatedApi.reducer,
    [publicApi.reducerPath]: publicApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(
      authenticatedApi.middleware,
      publicApi.middleware
    ),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
