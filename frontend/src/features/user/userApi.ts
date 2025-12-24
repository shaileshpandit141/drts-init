import { authenticatedApi } from "app/authenticatedApi";
import type { UserResponse } from "./types";
import { setUserState } from "./userSlice";

export const userApi = authenticatedApi.injectEndpoints({
  endpoints: (builder) => ({
    user: builder.query<UserResponse, void>({
      query: () => "/auth/user/",
      async onQueryStarted(_, { dispatch, queryFulfilled }) {
        try {
          const { data } = await queryFulfilled;
          dispatch(setUserState(data));
        } catch (err) {
          console.error("Failed to fetch user:", err);
        }
      },
    }),
  }),
});

export const { useUserQuery } = userApi;
