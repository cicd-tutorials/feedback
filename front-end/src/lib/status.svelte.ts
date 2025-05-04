import type { Problem } from "./api";

export interface Status {
  loading: boolean;
  error: Problem | null;
}

let status = $state<Status>({
  loading: true,
  error: null,
});

export const setLoading = (loading: boolean) => {
  status.loading = loading;
};

export const setError = (error: Problem | null) => {
  status.error = error;
};

export const getStatus = () => {
  return JSON.parse(JSON.stringify(status));
};
