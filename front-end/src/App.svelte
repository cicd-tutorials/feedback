<script lang="ts">
  import { onMount } from "svelte";

  import logo from "/logo.svg";
  import { getQuestion, waitUntilLive, type Question } from "./lib/api";
  import Loading from "./lib/Loading.svelte";
  import Error from "./lib/Error.svelte";
  import Footer from "./lib/Footer.svelte";
  import Share from "./views/Share.svelte";
  import { initializePath, parsePath, updatePath } from "./lib/path.svelte";
  import Link from "./lib/Link.svelte";
  import { getStatus, setError, setLoading } from "./lib/status.svelte";
  import Summary from "./views/Summary.svelte";
  import Form from "./views/Form.svelte";

  let { loading, error } = $derived.by(getStatus);
  let view = $derived.by(() => parsePath().view);
  let question = $state<Question | null>(null);

  const initializeQuestion = async () => {
    try {
      // Wait until the server has started.
      await waitUntilLive();

      const { key } = parsePath();
      if (!key) {
        setError({
          status: 400,
          title:
            "Question key is missing. Please ask for a valid link to the feedback form.",
        });
        return;
      }

      // Fetch the question using the key.
      const qr = await getQuestion(key);
      if (qr.error) {
        setError(qr.error);
        return;
      }
      question = qr.data;
    } catch (err) {
      setError({
        status: 500,
        title: "Failed to initialize feedback application.",
      });
    } finally {
      setLoading(false);
    }
  };

  onMount(() => {
    initializePath();
    initializeQuestion();

    window.addEventListener("popstate", () => {
      updatePath();
    });
  });

  $effect(() => {
    if (["form", "share", "summary"].includes(view) === false) {
      setError({
        status: 404,
        title: "Page not found",
      });
      return;
    }
  });
</script>

<header>
  <div>
    <img src={logo} class="logo" alt="Site logo" />
  </div>
  <h1>Feedback</h1>
</header>
<main>
  {#if loading}
    <Loading />
  {:else if error}
    <Error {error} />
  {/if}

  {#if question}
    {#if view === "form"}
      <Form {question} />
    {:else if view === "summary"}
      <Summary {question} />
    {:else if view === "share"}
      <Share {question} />
    {/if}
    <div class="links">
      {#if view !== "form"}
        <Link target={`/${question.key}`}>Submit an answer</Link>
      {/if}
      {#if view !== "share"}
        <Link target={`/${question.key}/share`}>Share the URL</Link>
      {/if}
      {#if view !== "summary"}
        {#if view === "share"}
          <Link target={`/${question.key}/summary`}>Hide the QR code</Link>
        {:else}
          <Link target={`/${question.key}/summary`}>View answer summary</Link>
        {/if}
      {/if}
    </div>
  {/if}
</main>
<Footer />

<style>
  header,
  main,
  :global(footer) {
    width: min(95%, 800px);
    margin: auto;
  }

  header {
    display: flex;
    gap: 1em;
    align-items: center;
    margin-bottom: 2em;
    height: 48px;

    border-bottom: 1px solid var(--color-border);
  }

  header .logo {
    width: 24px;
    height: 24px;
  }

  h1 {
    font-size: 18px;
    font-weight: 300;
    margin: 0;
  }

  main {
    flex: 1;
  }

  .links {
    color: var(--color-secondary);
    display: flex;
    gap: 1rem;
    margin: 3rem 0 2rem;
    /* Disable margins from collapsing */
    padding-top: 0.05px;
  }
</style>
