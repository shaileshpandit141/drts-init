import { fetchBaseQuery } from "@reduxjs/toolkit/query/react";

const BASE_URL = "http://localhost:8000/api/v1";

/**
 * Public API base query:
 * - No Authorization header
 * - Can be used for login, signup, or public endpoints
 */
export const baseQueryPublic = fetchBaseQuery({
  baseUrl: BASE_URL,
  prepareHeaders: (headers) => {
    headers.set("Content-Type", "application/json");
    return headers;
  },
});
