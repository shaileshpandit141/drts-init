export declare module "BaseAPITypes" {
  /**
   * API Meta Information
   */
  export interface Meta {
    rate_limits: {
      throttled_by: string | null;
      throttles: {
        [key: string]: ThrottleInfo;
      };
    };
  }

  export interface ThrottleInfo {
    limit: number;
    remaining: number;
    reset_time: string;
    retry_after: {
      time: number;
      unit: string;
    };
  }

  /**
   * General Error Structure
   */
  export interface Errors {
    detail?: string;
    code?: string;
    non_field?: string[];
    [key: string]: string[] | string | undefined;
  }

  /**
   * Base state structure for Redux slices
   */
  export interface BaseState {
    status: "idle" | "loading" | "succeeded" | "failed";
    status_code: number | null;
    message: string | null;
    meta: Meta | null;
  }

  /**
   * Generic state structure for Redux slices
   * Supports both `{}` and `[]` responses in `data`
   */
  export interface InitialState<
    DATA = Record<string, any> | Record<string, any>[],
    ERRORS,
  > extends BaseState {
    data: DATA | null;
    errors: (Errors & ERRORS) | null;
  }

  /**
   * State structure for paginated API responses
   */
  export interface PaginatedInitialState<
    DATA = Record<string, any>,
    ERRORS = Errors,
  > extends BaseState {
    data: {
      page: {
        current: number;
        total: number;
        size: number;
        total_items: pnumber;
        next: string | null;
        previous: string | null;
      };
      results: DATA[] | null;
    } | null;
    errors: (Errors & ERRORS) | null;
  }

  /**
   * Success response interface for API calls
   */
  export interface SuccessResponse<DATA = Record<string, any>>
    extends BaseState {
    status: "succeeded";
    data: DATA;
    errors: null;
  }

  /**
   * Error response interface for failed API calls
   */
  export interface ErrorResponse<ERRORS = Errors> extends BaseState {
    status: "failed";
    data: null;
    errors: (Errors & ERRORS) | null;
  }

  /**
   * Axios error catch structure containing error response data
   */
  export interface CatchAxiosError {
    response?: {
      data: ErrorResponse;
    };
    message?: string;
  }
}
