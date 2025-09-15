import { authenticatedApi } from "app/authenticatedApi";
import type { SigninRequest, SigninResponse } from "./types";
import type { SignoutRequest, SignoutResponse } from "./types";
import { setAuthState, signout } from "./authSlice";

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
          dispatch(setAuthState(data));
        } catch (err) {
          dispatch(signout());
          console.error("Failed to fetch signin tokens:", err);
        }
      },
    }),
    signout: builder.mutation<SignoutResponse, SignoutRequest>({
      query: (credentials) => ({
        url: "/auth/token/block/",
        method: "POST",
        body: credentials,
      }),
      async onQueryStarted(_, { dispatch, queryFulfilled }) {
        try {
          await queryFulfilled;
        } catch (err) {
          console.error("Failed to block signin tokens:", err);
        }
        dispatch(signout());
      },
    }),
  }),
});

export const { useSigninMutation, useSignoutMutation } = authApi;
