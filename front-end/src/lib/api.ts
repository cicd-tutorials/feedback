export const baseUrl = () => {
  try {
    // @ts-ignore: defined in config.js
    return serverUrl;
  } catch (_) {
    return "http://localhost:5000";
  }
}

export interface Question {
  key: string;
  text: string;
  type: string;
  with_comment: boolean;
}

export interface Answer {
  id: string;
  key: string;
  value: string;
  comment: string;
  submitted_at: string;
}

export interface Problem {
  title: string;
  status: number;
}

export interface APIResponse<T> {
  data: T;
  error: Problem;
}

const buildResponse = async <T>(Response: Response): Promise<APIResponse<T>> => {
  const data = await Response.json();
  return {
    data: Response.ok ? data : null,
    error: Response.ok ? null : data,
  };
}

export const getQuestion = async (key: string): Promise<APIResponse<Question>> => {
  const response = await fetch(`${baseUrl()}/feedback/${key}`);
  return buildResponse<Question>(response);
}

export const createAnswer = async (key: string): Promise<APIResponse<Answer>> => {
  const response = await fetch(`${baseUrl()}/feedback/${key}/answer`, {
    method: "POST",
    body: "{}",
    headers: {
      "Content-Type": "application/json",
    },
  });
  return buildResponse<Answer>(response);
}

export const updateAnswer = async (key: string, id: string, payload: Answer): Promise<APIResponse<Answer>> => {
  const response = await fetch(`${baseUrl()}/feedback/${key}/answer/${id}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
    headers: {
      "Content-Type": "application/json",
    },
  });
  return buildResponse<Answer>(response);
}
