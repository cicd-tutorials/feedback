<script lang="ts">
  import QRCode from "qrcode";

  import type { Question } from "../lib/api";
  import Summary from "./Summary.svelte";

  interface Props {
    question: Question;
  }

  let { question }: Props = $props();

  let copied = $state(false);

  const url = `${window.location.origin}/${question.key}`;

  $effect(() => {
    var style = window.getComputedStyle(document.documentElement);
    const light = style.getPropertyValue("--color-bg");
    const dark = style.getPropertyValue("--color-fg");
    const rem = parseFloat(style.fontSize);

    const canvas = document.getElementById("qrcode") as HTMLCanvasElement;
    QRCode.toCanvas(canvas, url, {
      color: {
        dark,
        light,
      },
      margin: 0,
      width: 12 * rem,
    });
  });

  const copyLink = async () => {
    try {
      await navigator.clipboard.writeText(url);
      copied = true;
      setTimeout(() => {
        copied = false;
      }, 1500);
    } catch {
      /* Ignore error */
    }
  };
</script>

<Summary {question} />
<div class="divider"></div>
<p>Scan the QR code to open the feedback form.</p>
<button class="qrcode-container" onclick={copyLink}>
  <canvas id="qrcode" title={url}></canvas>
  <div class="copy-message">
    {#if copied}Link copied!{:else}Click to copy the link.{/if}
  </div>
</button>

<style>
  p {
    margin: 1rem 0 2rem;
  }

  .divider {
    border: 1px solid var(--color-border);
    margin: 3rem 0 2rem;
  }

  .qrcode-container {
    display: inline-block;

    appearance: none;
    background: none;
    border: none;
    border-radius: var(--border-radius);
    color: inherit;
    margin: calc(var(--border-radius) * -1);
    padding: var(--border-radius);
  }

  .qrcode-container:focus-visible {
    outline: 2px solid var(--color-fg);
    outline-offset: 0.25rem;
  }

  .copy-message {
    font-size: 0.8rem;
    line-height: 1rem;
    text-align: center;
    opacity: 0;
  }

  .qrcode-container:hover .copy-message,
  .qrcode-container:focus-visible .copy-message {
    opacity: 1;
  }
</style>
