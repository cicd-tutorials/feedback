<script lang="ts">
  import type { Choice, Summary } from "./api";

  interface Props {
    choices: Choice[];
    summary: Summary;
  }

  let { choices, summary }: Props = $props();
</script>

<div class="bar-chart">
  {#each choices as choice}
    <div class="row">
      <span>{choice.label}</span>
      <div class="bar" style="width: {summary.values[String(choice.value)] / summary.count_non_null * 100}%"
        ></div>
      <span>{summary.values[String(choice.value)]}</span>
    </div>
  {/each}
</div>

<style>
  .bar-chart {
    margin: 2rem 0;
  }

  .row {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 1rem 0;
  }

  .bar {
    background-color: var(--color-primary);
    border-radius: var(--border-radius);
    height: 0.5rem;
    min-width: 1rem;
  }
</style>
