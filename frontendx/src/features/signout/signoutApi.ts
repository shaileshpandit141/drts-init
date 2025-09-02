import { createApi } from "@reduxjs/toolkit/query/react";
import type { SignoutRequest, SignoutResponse } from "./types";
import { baseQueryAuth } from "app/baseQueryAuth";
import { signout } from "features/auth/authSlice";
import { setSignoutState } from "./signoutSlice";

export const signoutApi = createApi({
  reducerPath: "signoutApi",
  baseQuery: baseQueryAuth,
  endpoints: (builder) => ({
    signout: builder.mutation<SignoutResponse, SignoutRequest>({
      query: (credentials) => ({
        url: "/auth/token/block/",
        method: "POST",
        body: credentials,
      }),
      async onQueryStarted(_, { dispatch, queryFulfilled }) {
        try {
          const { data } = await queryFulfilled;
          dispatch(
            setSignoutState({
              detail: data.detail,
            })
          );
          dispatch(signout());
        } catch {
          dispatch(signout());
        }
      },
    }),
  }),
});

export const { useSignoutMutation } = signoutApi;
