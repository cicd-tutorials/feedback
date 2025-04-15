<script lang="ts">
  import RadioGroup from "./RadioGroup.svelte";

  interface Props {
    onChange: (value: number) => void;
    value?: number;
  }

  let { onChange, value }: Props = $props();

  const items = [
    {
      value: -1,
      label: "👎",
      title: "Thumbs down",
    },
    {
      value: 1,
      label: "👍",
      title: "Thumbs up",
    },
  ];
</script>

<RadioGroup {items} name="thumbs" {onChange} {value} />
