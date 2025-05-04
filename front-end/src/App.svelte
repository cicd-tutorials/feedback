<script lang="ts">
  import { onMount } from "svelte";

  import logo from "/logo.svg";
  import RadioGroup from "./lib/RadioGroup.svelte";
  import {
    createAnswer,
    getAnswer,
    getQuestion,
    getSummary,
    updateAnswer,
    waitUntilLive,
    type Answer,
    type Problem,
    type Question,
    type Summary,
    type UpdateAnswerPayload,
  } from "./lib/api";
  import Loading from "./lib/Loading.svelte";
  import Error from "./lib/Error.svelte";
  import Submit from "./lib/Submit.svelte";
  import Comment from "./lib/Comment.svelte";
  import BarChart from "./lib/BarChart.svelte";
  import Footer from "./lib/Footer.svelte";
  import Share from "./views/Share.svelte";
  import { initializePath, navigate, parsePath } from "./lib/path.svelte";
  import Link from "./lib/Link.svelte";

  let loading = $state(true);
  let view = $derived.by(() => parsePath().view);
  let error = $state<Problem | null>(null);
  let question = $state<Question | null>(null);
  let answer = $state<Answer | null>(null);
  let summary = $state<Summary | null>(null);

  const initAnswer = async () => {
    try {
      // Wait until the server has started.
      await waitUntilLive();

      const { key, view, id } = parsePath();
      if (!key) {
        error = {
          status: 404,
          title: "Question not found",
        };
        return;
      }

      if (["form", "share", "summary"].includes(view) === false) {
        error = {
          status: 404,
          title: "Page not found",
        };
        return;
      }

      // Fetch the question using the key.
      const qr = await getQuestion(key);
      if (qr.error) {
        error = qr.error;
        return;
      }
      question = qr.data;

      // Initialize new answer or get existings answer.
      if (view === "form") {
        const ar = id ? await getAnswer(id) : await createAnswer(key);
        if (ar.error) {
          error = ar.error;
          return;
        }
        answer = ar.data;
        navigate(`/${key}?id=${answer.id}`, true);
      }

      // Fetch the summary.
      if (view === "summary") {
        fetchSummary(key);
      }
    } catch (err) {
      error = {
        status: 500,
        title: "Failed to initialize feedback form.",
      };
    } finally {
      loading = false;
    }
  };

  onMount(() => {
    initializePath();

    window.addEventListener("popstate", () => {
      initAnswer();
    });

    initAnswer();
  });

  $effect(() => {
    if (view === "form" && answer === null) {
      initAnswer();
    }
  });

  const handleChange = async (payload: UpdateAnswerPayload) => {
    if (!answer) {
      return;
    }

    try {
      const ar = await updateAnswer(answer?.id, payload);
      if (ar.error) {
        error = ar.error;
        return;
      }
      answer = ar.data;
    } catch (_) {
      error = {
        status: 500,
        title: "Failed to update feedback.",
      };
    }
  };

  const fetchSummary = async (key?: string) => {
    loading = true;
    try {
      const sr = await getSummary(key ?? "");
      if (sr.error) {
        error = sr.error;
        return;
      }
      summary = sr.data;
    } catch (_) {
      error = {
        status: 500,
        title: "Failed to fetch summary.",
      };
    } finally {
      loading = false;
    }
  };

  const handleSubmit = async () => {
    loading = true;
    await handleChange({ submit: true });
    navigate(`/${answer?.key}/summary`);
    await fetchSummary(answer?.key);
    answer = null;
    loading = false;
  };
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
  {:else if question && view === "form"}
    <fieldset>
      <legend>{question.choice_text}</legend>
      <RadioGroup
        items={question.choices}
        name={question.type}
        onChange={(value) => handleChange({ value })}
        value={answer?.value}
      />
    </fieldset>
    {#if answer?.value != undefined}
      {#if question?.with_comment}
        <Comment
          label={question?.comment_text}
          onChange={(comment) => handleChange({ comment })}
          value={answer?.comment}
        />
      {/if}
      <Submit onSubmit={handleSubmit} />
    {/if}
  {:else if question && view === "summary" && summary}
    <div class="summary">
      <p>Thank you for your feedback!</p>
      <BarChart choices={question.choices} {summary} />
    </div>
  {:else if question && view === "share"}
    <Share {question} />
  {/if}
  {#if question}
    <div class="links">
      {#if view !== "form"}
        <Link target={`/${question.key}`}>Submit an answer</Link>
      {/if}
      {#if view !== "share"}
        <Link target={`/${question.key}/share`}>Share the URL</Link>
      {/if}
      {#if view !== "summary"}
        <Link target={`/${question.key}/summary`}>View answer summary</Link>
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

  fieldset {
    appearance: none;
    border: none;
    margin: 0;
    padding: 0;
  }

  legend {
    appearance: none;
    margin: 1rem 0;
    padding: 0;
  }

  .links {
    display: flex;
    gap: 1rem;
    margin: 2rem 0;
    /* Disable margins from collapsing */
    padding-top: 0.05px;
  }
</style>
