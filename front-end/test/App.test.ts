import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/svelte";

import App from "../src/App.svelte";

it("renders without errors", async () => {
  render(App);

  await screen.findByText("Loading");
});
