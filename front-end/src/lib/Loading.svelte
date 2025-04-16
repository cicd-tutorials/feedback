<div class="loading">
  <div class="status">
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="dot"></div>
  </div>
  <div class="title">Loading</div>
</div>

<style>
  .status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem 0;
  }

  .dot {
    background-color: var(--color-primary);
    border-radius: 50%;
    height: 0.5rem;
    width: 0.5rem;

    animation: loading 2s infinite;
  }

  .dot:nth-child(2) {
    animation-delay: 250ms;
  }
  .dot:nth-child(3) {
    animation-delay: 500ms;
  }

  @keyframes loading {
    0%,
    62.5%,
    100% {
      opacity: 0;
    }

    12.5%,
    50% {
      opacity: 1;
    }
  }

  .title {
    font-size: 1rem;
    line-height: 1.5rem;
  }
</style>
