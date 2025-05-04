<script lang="ts">
  import { onMount } from "svelte";

  import { type Question } from "../lib/api";
  import BarChart from "../lib/BarChart.svelte";
  import { getStatus } from "../lib/status.svelte";
  import { getSummary, fetchSummary } from "../lib/summary.svelte";

  interface Props {
    question: Question;
  }

  let { question }: Props = $props();

  let { loading, error } = $derived.by(getStatus);
  let summary = $derived.by(getSummary);

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

{#if !loading && !error && summary}
  <p>{question.choice_text}</p>
  <BarChart choices={question.choices} {summary} />
{/if}

<style>
  p {
    margin: 1rem 0 2rem;
  }
</style>
