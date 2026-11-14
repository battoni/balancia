interface PaginatorLinks {
  active: boolean;
  label: string;
  url: string | null;
}

interface PaginateResult<T = any> {
  current_page: number;
  data: T[];
  first_page_url: string;
  from: number;
  last_page: number;
  last_page_url: string;
  links: PaginatorLinks[];
  next_page_url: string | null;
  path: string;
  per_page: number;
  prev_page_url: string | null;
  to: number;
  total: number;
}

type ApiQueryValue = string | number | boolean | undefined | null;

type ApiQuery = Record<string, ApiQueryValue | ApiQueryValue[]>;

interface ApiParams {
  endpoint: string;
  forwardError?: boolean;
  /** Merged over the defaults — how a service sends a header of its own (a token, a locale). */
  headers?: Record<string, string>;
  isUpload?: boolean;
  method?: 'get' | 'post' | 'delete' | 'patch' | 'put';
  /**
   * The read is the PAGE's, not a screen's: the route guard's abort-on-navigation leaves it alone. Only for
   * app-wide state a navigation must not lose (the host firm's brand, read again on a logout that also
   * pushes the login — Chrome QA 5.21).
   */
  outlivesNavigation?: boolean;
  payload?: any;
  query?: ApiQuery;
}

interface ApiResponse<T = any> {
  data: T;
}

export type { ApiParams, ApiQuery, ApiQueryValue, ApiResponse, PaginateResult };
