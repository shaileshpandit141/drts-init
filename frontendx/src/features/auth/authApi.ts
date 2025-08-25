import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import type {
  SigninRequest,
  SigninResponse,
} from "./types";
import { setCredentials, signout } from "./authSlice";
import type { RootState } from "../../app/store";

const BASE_URL = "http://localhost:8000/api/v1";

export const authApi = createApi({
  reducerPath: "authApi",
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_URL,
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.access_token;
      if (token) {
        headers.set("Authorization", `Bearer ${token}`);
      }
      return headers;
    },
  }),
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
