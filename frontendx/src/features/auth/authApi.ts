import { authenticatedApi } from "app/authenticatedApi";
import type { SigninRequest, SigninResponse } from "./types";
import { setCredentials, signout } from "./authSlice";

export const authApi = authenticatedApi.injectEndpoints({
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
