import { authenticatedApi } from "app/authenticatedApi";
import type { SignoutRequest, SignoutResponse } from "./types";
import { signout } from "features/auth/authSlice";
import { setSignoutState } from "./signoutSlice";

export const signoutApi = authenticatedApi.injectEndpoints({
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
        } catch (err) {
          dispatch(signout());
          console.error("Failed to block signin tokens:", err);
        }
      },
    }),
  }),
});

export const { useSignoutMutation } = signoutApi;
