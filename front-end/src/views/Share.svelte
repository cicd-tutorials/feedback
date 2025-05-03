<script lang="ts">
  import QRCode from "qrcode";

  import type { Question } from "../lib/api";

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

<div class="share">
  <p>{question.choice_text} Scan the QR code to open the feedback form.</p>
  <canvas id="qrcode"></canvas>
</div>

<style>
  canvas {
    margin: 2rem 0;
  }
</style>
