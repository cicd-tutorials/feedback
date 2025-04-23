<script lang="ts">
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-ignore
  const build = import.meta.env.VITE_BUILD ?? "";
</script>

<footer>
  <a href="https://github.com/cicd-tutorials/feedback.git" target="_blank">
    Source code
  </a>
  {#if build}
    <span>Build {build}</span>
  {/if}
</footer>

<style>
  footer {
    display: flex;
    justify-content: space-between;

    color: var(--color-secondary);
    font-size: 0.85rem;
    border-top: 1px solid var(--color-border);
    padding: 0.5rem 0;
  }
</style>
