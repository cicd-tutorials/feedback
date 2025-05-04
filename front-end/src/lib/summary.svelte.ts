import { getSummary as _getSummary, type Summary } from "./api";
import { setError, setLoading } from "./status.svelte";

let summary = $state<Summary | null>(null);

export const fetchSummary = async (key?: string) => {
  if (summary === null) {
    setLoading(true);
  }

  try {
    const sr = await _getSummary(key ?? "");
    if (sr.error) {
      setError(sr.error);
      return;
    }
    summary = sr.data;
  } catch (_) {
    setError({
      status: 500,
      title: "Failed to fetch summary.",
    });
  } finally {
    setLoading(false);
  }
};

export const getSummary = () => {
  return summary;
};
