<script lang="ts">
  import { onMount } from "svelte";

  import logo from "/logo.svg";
  import RadioGroup from "./lib/RadioGroup.svelte";
  import {
    createAnswer,
    getQuestion,
    getSummary,
    updateAnswer,
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

  let loading = $state(true);
  let error = $state<Problem | null>(null);
  let question = $state<Question | null>(null);
  let answer = $state<Answer | null>(null);
  let summary = $state<Summary | null>(null);

  onMount(() => {
    const initAnswer = async () => {
      try {
        // Parse the question key from URL query parameters
        const query = new URLSearchParams(window.location.search);
        const key = query.get("key");
        if (!key) {
          error = {
            status: 404,
            title: "Question not found",
          };
          return;
        }

        // Fetch the question using the key
        const qr = await getQuestion(key);
        if (qr.error) {
          error = qr.error;
          return;
        }
        question = qr.data;

        // Initialize the answer
        const ar = await createAnswer(key);
        if (ar.error) {
          error = ar.error;
          return;
        }
        answer = ar.data;
      } catch (err) {
        error = {
          status: 500,
          title: "Failed to initialize feedback form.",
        };
      } finally {
        loading = false;
      }
    };

    initAnswer();
  });

  const handleChange = async (payload: UpdateAnswerPayload) => {
    if (!answer) {
      return;
    }

    try {
      const ar = await updateAnswer(answer?.key, answer?.id, payload);
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

  const handleSubmit = async () => {
    loading = true;
    await handleChange({ submit: true });
    try {
      const sr = await getSummary(answer?.key ?? "");
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
  {:else if question && !answer?.submitted_at}
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
  {:else if question && answer?.submitted_at && summary}
    <div class="summary">
      <p>Thank you for your feedback!</p>
      <BarChart choices={question.choices} {summary} />
    </div>
  {/if}
</main>

<style>
  header,
  main {
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
</style>
