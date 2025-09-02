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
  }),
});

export const { useSigninMutation } = authApi;
