import { publicApi } from "app/publicApi";
import type { SignupRequest, SignupResponse } from "./types";

export const authApi = publicApi.injectEndpoints({
  endpoints: (builder) => ({
    signup: builder.mutation<SignupResponse, SignupRequest>({
      query: (credentials) => ({
        url: "/auth/signup/",
        method: "POST",
        body: credentials,
      }),
      async onQueryStarted(_, { dispatch, queryFulfilled }) {
        try {
          await queryFulfilled;
        } catch (error) {
          console.error("Sign up request failed:", error);
        }
      },
    }),
  }),
});

export const { useSignupMutation } = authApi;
