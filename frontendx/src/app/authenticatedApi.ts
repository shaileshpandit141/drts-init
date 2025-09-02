import {
  createApi,
  fetchBaseQuery,
  type FetchArgs,
  type FetchBaseQueryError,
  type BaseQueryFn,
} from "@reduxjs/toolkit/query/react";
import type { RootState } from "./store";
import { BASE_API_URL } from "./baseApiUrl";
import { setCredentials, signout } from "features/auth/authSlice";

// base query with token in headers
const rawBaseQuery = fetchBaseQuery({
  baseUrl: BASE_API_URL,
  prepareHeaders: (headers, { getState }) => {
    const token = (getState() as RootState).auth.access_token;
    if (token) {
      headers.set("Authorization", `Bearer ${token}`);
    }
    return headers;
  },
});

// wrapper to handle token refresh
const baseQueryWithReauth: BaseQueryFn<
  string | FetchArgs,
  unknown,
  FetchBaseQueryError
> = async (args, api, extraOptions) => {
  let result = await rawBaseQuery(args, api, extraOptions);

  if (result.error && result.error.status === 401) {
    const refresh_token = (api.getState() as RootState).auth.refresh_token;

    // try refreshing the token
    if (refresh_token) {
      const refreshResult = await fetch(`${BASE_API_URL}/auth/token/refresh/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ refresh_token }),
      }).then((res) => res.json());

      if (refreshResult?.access_token) {
        api.dispatch(
          setCredentials({
            access_token: refreshResult.access_token,
            refresh_token,
          })
        );

        // retry original query with updated token
        result = await rawBaseQuery(args, api, extraOptions);
      } else {
        api.dispatch(signout());
      }
    } else {
      api.dispatch(signout());
    }
  }

  return result;
};

export const authenticatedApi = createApi({
  reducerPath: "authenticatedApi",
  baseQuery: baseQueryWithReauth,
  endpoints: () => ({}), // leave empty, inject later
});
