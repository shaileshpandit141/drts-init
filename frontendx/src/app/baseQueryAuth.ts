import { fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import type { RootState } from "./store";
// import { store } from "./store";
// import { signout } from "../features/auth/authSlice";

const BASE_URL = "http://localhost:8000/api/v1";

/**
 * Common baseQuery for all protected APIs
 * Handles:
 * - JWT in headers
 * - 401 auto-signout
 */
export const baseQueryAuth = fetchBaseQuery({
  baseUrl: BASE_URL,
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
});
