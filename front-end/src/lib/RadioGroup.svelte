<script lang="ts">
  interface Props {
    items: {
      value: number;
      label: string;
      title: string;
    }[];
    name: string;
    onChange: (value: number) => void;
    value?: number;
  }

  let { items, name, onChange, value }: Props = $props();
  let selectedValue = $state<number>();

  $effect(() => {
    if (value) {
      selectedValue = value;
    }
  });

  $effect(() => {
    if (selectedValue && selectedValue !== value) {
      onChange(selectedValue);
    }
  });
</script>

<div class="radio-group">
  {#each items as item}
    <label class="item" for="{name}-{item.value}" title={item.title}>
      <input
        id="{name}-{item.value}"
        {name}
        type="radio"
        value={item.value}
        bind:group={selectedValue}
      />
      <div class="label">{item.label}</div>
    </label>
  {/each}
</div>

<style>
  .radio-group {
    display: flex;
    gap: 1rem;
  }

  .item {
    border: 1px solid var(--color-border);
    border-radius: var(--border-radius);
    box-sizing: border-box;
    position: relative;
    padding: 0.75rem 1.25rem;

    transition: transform 0.1s ease-in-out;
  }

  .item:has(:checked) {
    border-color: var(--color-fg);
  }

  .item:has(:focus-visible) {
    outline: 2px solid var(--color-fg);
    outline-offset: 0.25rem;
  }

  .item:hover {
    transform: translateY(-0.1rem);
  }

  .item:active {
    transform: translateY(0.15rem);
  }

  input[type="radio"] {
    position: absolute;
    top: 4px;
    left: 4px;
    margin: 0;

    appearance: none;
    height: 0.375rem;
    width: 0.375rem;
  }

  input[type="radio"]:focus {
    outline: none;
  }

  input[type="radio"]:checked {
    display: block;
    background: var(--color-fg);
    border-radius: 50%;
  }
</style>
