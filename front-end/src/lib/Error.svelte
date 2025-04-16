<script lang="ts">
  import type { Problem } from "./api";

  interface Props {
    error: Problem;
  }

  let { error }: Props = $props();
</script>

<div class="error">
  <span class="status">{error.status}</span>
  <div class="title">{error.title}</div>
</div>

<style>
  .error {
    margin-top: 1rem;
  }

  .status {
    background-color: var(--color-error);
    color: var(--color-bg);

    line-height: 2rem;
    font-size: 2rem;
    padding: 0 0.25rem;
    border-radius: var(--border-radius);
  }

  .title {
    font-size: 1rem;
    line-height: 1.5rem;
    margin-top: 0.5rem;
  }
</style>
