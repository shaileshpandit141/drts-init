import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import type { RootState } from "./store";
import { BASE_API_URL } from "./baseApiUrl";

export const authenticatedApi = createApi({
  reducerPath: "authenticatedApi",
  baseQuery: fetchBaseQuery({
    baseUrl: BASE_API_URL,
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.access_token;
      if (token) headers.set("Authorization", `Bearer ${token}`);
      return headers;
    },
    // Handle 401 globally
    async fetchFn(input, init) {
      const result = await fetch(input, init);
      if (result.status === 401) {
        // store.dispatch(signout());
      }
      return result;
    },
  }),
  endpoints: () => ({}), // leave empty, inject later
});
