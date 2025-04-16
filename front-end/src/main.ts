import { mount } from "svelte";
import "./global.css";
import "./theme.css";
import App from "./App.svelte";

const app = mount(App, {
  target: document.querySelector("body")!,
});

export default app;
