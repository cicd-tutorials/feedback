<script lang="ts">
  import { onMount } from "svelte";

  import logo from "/logo.svg";
  import Thumbs from "./lib/Thumbs.svelte";
  import {
    createAnswer,
    getQuestion,
    type Answer,
    type Problem,
    type Question,
  } from "./lib/api";
  import Loading from "./lib/Loading.svelte";
  import Error from "./lib/Error.svelte";

  let loading = $state(true);
  let error = $state<Problem | null>(null);
  let question = $state<Question | null>(null);
  let answer = $state<Answer | null>(null);

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

  const handleSelect = (value: number) => {};
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
  {:else if question}
    <div class="question">
      <p>{question.text}</p>
      <Thumbs onSelect={handleSelect} />
    </div>
  {/if}
</main>

<style>
  header,
  main {
    padding: 0 1em;
    max-width: 800px;
    margin: auto;
  }

  header {
    display: flex;
    gap: 1em;
    align-items: center;
    margin-bottom: 2em;
    height: 48px;
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
</style>
