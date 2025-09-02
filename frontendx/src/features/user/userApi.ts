import { createApi } from "@reduxjs/toolkit/query/react";
import type { UserResponse } from "./types";
import { baseQueryAuth } from "app/baseQueryAuth";
import { setUserState } from "./userSlice";

export const userApi = createApi({
  reducerPath: "userApi",
  baseQuery: baseQueryAuth,
  endpoints: (builder) => ({
    user: builder.mutation<UserResponse, void>({
      query: () => ({
        url: "/auth/user/",
        method: "GET",
      }),
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

export const { useUserMutation } = userApi;
