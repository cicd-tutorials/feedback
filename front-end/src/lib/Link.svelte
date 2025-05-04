<script lang="ts">
  import type { Snippet } from "svelte";
  import { navigate } from "./path.svelte";

  interface Props {
    children: Snippet;
    target: string;
  }

  let { children, target }: Props = $props();
</script>

<a
  href={target}
  onclick={(event) => {
    navigate(target);
    event.preventDefault();
  }}>{@render children?.()}</a
>
