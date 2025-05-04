export interface QuestionPath {
  key: string;
  view: string;
  id?: string;
}

let path = $state<string>("");

export const updatePath = () => {
  path = window.location.pathname;
};

export const initializePath = () => {
  updatePath();
  const { key } = parsePath();

  // Replace path if key is given as query parameter instead of path parameter. This is for backwards compatibility.
  const query = new URLSearchParams(window.location.search);
  const queryKey = query.get("key");
  if (queryKey && !key) {
    navigate(`/${queryKey}`, true);
  }
};

export const parsePath = (): QuestionPath => {
  const pathComponents = path.split("/").slice(1);
  const query = new URLSearchParams(window.location.search);

  const key = pathComponents[0] ?? "";
  const view = pathComponents[1] || "form";
  const id = query.get("id") ?? undefined;

  return { key, view, id };
};

export const navigate = (next: string, replace = false) => {
  if (replace) {
    window.history.replaceState({}, "", next);
  } else {
    window.history.pushState({}, "", next);
  }
  path = next;
};
