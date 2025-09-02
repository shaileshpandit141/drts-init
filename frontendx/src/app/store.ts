import { configureStore } from "@reduxjs/toolkit";
import toastReducer from "features/toast/toastSlice";
import { authApi } from "features/auth/authApi";
import authReducer from "features/auth/authSlice";
import signoutReducer from "features/signout/signoutSlice";
import { signoutApi } from "features/signout/signoutApi";
import { userSlice } from "features/user/userSlice";
import { userApi } from "features/user/userApi";

export const store = configureStore({
  reducer: {
    toast: toastReducer,
    auth: authReducer,
    [authApi.reducerPath]: authApi.reducer,
    signout: signoutReducer,
    [signoutApi.reducerPath]: signoutApi.reducer,
    user: userSlice.reducer,
    [userApi.reducerPath]: userApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(
      authApi.middleware,
      signoutApi.middleware,
      userApi.middleware
    ),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
