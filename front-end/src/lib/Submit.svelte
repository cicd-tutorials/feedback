<script lang="ts">
  interface Props {
    onSubmit: () => void;
  }

  let { onSubmit }: Props = $props();
</script>

<button type="button" onclick={onSubmit}>Submit</button>

<style>
  button {
    appearance: none;
    background-color: var(--color-primary);
    border: none;
    border-radius: var(--border-radius);
    box-shadow: 0 0.1rem 0.25rem rgba(0, 0, 0, 0.5);
    color: var(--color-fg);
    font-weight: 500;
    letter-spacing: 0.5px;
    margin: 2rem 0;
    padding: 0.5rem 1rem;

    transition:
      box-shadow 0.1s ease-in-out,
      transform 0.1s ease-in-out;
  }

  button:hover {
    box-shadow: 0 0.2rem 0.25rem rgba(0, 0, 0, 0.5);
    transform: translateY(-0.1rem);
  }

  button:active {
    box-shadow: 0 0 0.25rem rgba(0, 0, 0, 0.5);
    transform: translateY(0.1rem);
  }

  button:focus-visible {
    outline: 2px solid var(--color-fg);
    outline-offset: 0.25rem;
  }
</style>
