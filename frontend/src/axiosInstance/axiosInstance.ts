/**
 * Axios instance configuration with authentication interceptors
 * Handles automatic token injection and refresh functionality
 */
import axios from "axios";
import { store } from "store/store";
import { refreshToken, resetSigninUser } from "features/auth/signin";
import { getBaseAPIURL } from "utils/getBaseAPIURL";

const axiosInstance = axios.create({
  baseURL: getBaseAPIURL(),
  timeout: 1000,
});

// Request interceptor - adds auth token to requests if available
axiosInstance.interceptors.request.use(
  (config) => {
    const token = store.getState().signin.data?.access_token;
    if (token) {
      config.headers = config.headers || {};
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const request = error.config;

    if (error.response?.status === 401 && !request._retry) {
      request._retry = true;

      try {
        // Call refreshToken (it updates Redux state internally)
        refreshToken();

        // Wait for Redux store to update before getting the new token
        return new Promise((resolve) => {
          const checkTokenUpdate = setInterval(() => {
            const token = store.getState().signin.data?.access_token;
            if (token) {
              clearInterval(checkTokenUpdate);
              request.headers["Authorization"] = `Bearer ${token}`;
              resolve(axiosInstance(request)); // Retry request with new token
            }
          }, 100); // Check every 100ms until token updates
        });
      } catch (refreshError) {
        resetSigninUser();
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  },
);

export default axiosInstance;
