import { createApi } from "@reduxjs/toolkit/query/react";
import type { SigninRequest, SigninResponse } from "./types";
import { setCredentials, signout } from "./authSlice";
import { baseQueryAuth } from "app/baseQueryAuth";

export const authApi = createApi({
  reducerPath: "authApi",
  baseQuery: baseQueryAuth,
  endpoints: (builder) => ({
    signin: builder.mutation<SigninResponse, SigninRequest>({
      query: (credentials) => ({
        url: "/auth/token/",
        method: "POST",
        body: credentials,
      }),
      async onQueryStarted(_, { dispatch, queryFulfilled }) {
        try {
          const { data } = await queryFulfilled;
          dispatch(setCredentials(data));
        } catch {
          dispatch(signout());
        }
      },
    }),
    refreshToken: builder.mutation<{ access: string }, { refresh: string }>({
      query: (body) => ({
        url: "/auth/token/refresh/",
        method: "POST",
        body,
      }),
      async onQueryStarted(arg, { dispatch, queryFulfilled }) {
        try {
          const { data } = await queryFulfilled;
          dispatch(
            setCredentials({
              access_token: data.access,
              refresh_token: arg.refresh,
            })
          );
        } catch {
          dispatch(signout());
        }
      },
    }),
  }),
});

export const { useSigninMutation, useRefreshTokenMutation } = authApi;
