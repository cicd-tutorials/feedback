<script lang="ts">
  import QRCode from "qrcode";

  import type { Question } from "../lib/api";
  import Summary from "./Summary.svelte";

  interface Props {
    question: Question;
  }

  let { question }: Props = $props();

  $effect(() => {
    var style = window.getComputedStyle(document.documentElement);
    const light = style.getPropertyValue("--color-bg");
    const dark = style.getPropertyValue("--color-fg");
    const rem = parseFloat(style.fontSize);

    const canvas = document.getElementById("qrcode") as HTMLCanvasElement;
    QRCode.toCanvas(canvas, `${window.location.origin}/${question.key}`, {
      color: {
        dark,
        light,
      },
      margin: 0,
      width: 16 * rem,
    });
  });
</script>

<Summary {question} />
<div class="divider"></div>
<p>Scan the QR code to open the feedback form.</p>
<canvas id="qrcode"></canvas>

<style>
  .divider {
    border: 1px solid var(--color-border);
    margin: 3rem 0 2rem;
  }

  canvas {
    margin: 2rem 0 0;
  }
</style>
