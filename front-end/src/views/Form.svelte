<script lang="ts">
  import { onMount } from "svelte";

  import RadioGroup from "../lib/RadioGroup.svelte";
  import {
    createAnswer,
    getAnswer,
    updateAnswer,
    type Answer,
    type Question,
    type UpdateAnswerPayload,
  } from "../lib/api";
  import Submit from "../lib/Submit.svelte";
  import Comment from "../lib/Comment.svelte";
  import { navigate, parsePath } from "../lib/path.svelte";
  import { getStatus, setError, setLoading } from "../lib/status.svelte";

  interface Props {
    question: Question;
  }

  let { question }: Props = $props();

  let answer = $state<Answer | null>(null);
  let { loading, error } = $derived.by(getStatus);

  const initAnswer = async () => {
    try {
      const { key, id } = parsePath();
      if (!key) {
        setError({
          status: 404,
          title: "Question not found",
        });
        return;
      }

      // Initialize new answer or get existings answer.
      const ar = id ? await getAnswer(id) : await createAnswer(key);
      if (ar.error) {
        setError(ar.error);
        return;
      }
      answer = ar.data;
      navigate(`/${key}?id=${answer.id}`, true);
    } catch (err) {
      setError({
        status: 500,
        title: "Failed to initialize feedback form.",
      });
    } finally {
      setLoading(false);
    }
  };

  onMount(() => {
    initAnswer();
  });

  const handleChange = async (payload: UpdateAnswerPayload) => {
    if (!answer) {
      return;
    }

    try {
      const ar = await updateAnswer(answer?.id, payload);
      if (ar.error) {
        setError(ar.error);
        return;
      }
      answer = ar.data;
    } catch (_) {
      setError({
        status: 500,
        title: "Failed to update feedback.",
      });
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    await handleChange({ submit: true });
    navigate(`/${answer?.key}/summary`);
    answer = null;
    // Summary view will set loading to false after updating the summary.
  };
</script>

{#if !loading && !error}
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
    <div class="submit">
      <Submit onSubmit={handleSubmit} />
    </div>
  {/if}
{/if}

<style>
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

  .submit {
    margin: 2rem 0 0;
  }
</style>
