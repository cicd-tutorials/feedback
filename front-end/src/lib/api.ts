export const baseUrl = () => {
  try {
    // @ts-ignore: defined in config.js
    return serverUrl.replace(/\/+$/, ""); // Remove trailing slashes
  } catch (_) {
    return "http://localhost:5000";
  }
};

export interface Choice {
  label: string;
  value: number;
  title: string;
}

export interface Question {
  key: string;
  type: string;
  choice_text: string;
  with_comment: boolean;
  comment_text: string;
  choices: Choice[];
}

export interface Answer {
  id: string;
  key: string;
  value: number;
  comment: string;
  group: string;
  submitted_at: string;
}

export type UpdateAnswerPayload = Partial<
  Pick<Answer, "value" | "comment" | "group"> & { submit: boolean }
>;

export interface Summary {
  count_non_null: number;
  count_total: number;
  values: Record<string, number>;
}

export interface Problem {
  title: string;
  status: number;
}

export interface APIResponse<T> {
  data: T;
  error: Problem;
}

const buildResponse = async <T>(
  Response: Response,
): Promise<APIResponse<T>> => {
  const data = await Response.json();
  return {
    data: Response.ok ? data : null,
    error: Response.ok ? null : data,
  };
};

export const getQuestion = async (
  key: string,
): Promise<APIResponse<Question>> => {
  const response = await fetch(`${baseUrl()}/question/${key}`);
  return buildResponse<Question>(response);
};

export const createAnswer = async (
  key: string,
): Promise<APIResponse<Answer>> => {
  const response = await fetch(`${baseUrl()}/question/${key}/answer`, {
    method: "POST",
    body: "{}",
    headers: {
      "Content-Type": "application/json",
    },
  });
  return buildResponse<Answer>(response);
};

export const updateAnswer = async (
  key: string,
  id: string,
  payload: UpdateAnswerPayload,
): Promise<APIResponse<Answer>> => {
  const response = await fetch(`${baseUrl()}/answer/${id}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
    headers: {
      "Content-Type": "application/json",
    },
  });
  return buildResponse<Answer>(response);
};

export const getSummary = async (
  key: string,
): Promise<APIResponse<Summary>> => {
  const response = await fetch(`${baseUrl()}/question/${key}/summary`);
  return buildResponse<Summary>(response);
};

export const waitUntilLive = async (): Promise<void> => {
  try {
    const response = await fetch(`${baseUrl()}/live`);
    if (response.status === 200) {
      return;
    }
  } catch (_) {
    // CORS requests will fail because of missing CORS headers until the server is live.
  }
  await new Promise((resolve) => setTimeout(resolve, 2500));
  return waitUntilLive();
};
