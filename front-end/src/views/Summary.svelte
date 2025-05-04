<script lang="ts">
  import { onMount } from "svelte";

  import { getSummary, type Question, type Summary } from "../lib/api";
  import BarChart from "../lib/BarChart.svelte";
  import { setError, setLoading } from "../lib/status.svelte";

  interface Props {
    question: Question;
  }

  let { question }: Props = $props();

  let summary = $state<Summary | null>(null);

  const fetchSummary = async (key?: string) => {
    if (summary === null) {
      setLoading(true);
    }

    try {
      const sr = await getSummary(key ?? "");
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

  onMount(() => {
    fetchSummary(question.key);

    // Refresh the summary every 5 seconds.
    const interval = setInterval(() => {
      fetchSummary(question.key);
    }, 5000);

    return () => {
      clearInterval(interval);
    };
  });
</script>

{#if summary}
  <div class="summary">
    <p>Thank you for your feedback!</p>
    <BarChart choices={question.choices} {summary} />
  </div>
{/if}
