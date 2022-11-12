"use strict";

function baseUrl() {
  try {
    return serverUrl;
  } catch (_) {
    return "http://localhost:5000";
  }
}

async function sendFeedback(type) {
  // Post feedback
  // We will ignore possible fetch errors and non-ok HTTP status codes here and later
  await fetch(`${baseUrl()}/feedback`, {
    method: "POST",
    mode: "cors",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ type }),
  });

  // Get feedback summary
  const res = await fetch(`${baseUrl()}/feedback/summary`, {
    mode: "cors",
  });

  if (!res.ok) {
    return;
  }

  // Hide buttons and display results summary
  document.getElementById("buttons-container").classList.add("hidden");
  document.getElementById("results-container").classList.remove("hidden");

  // Set bar chart bar width and count
  const results = await res.json();
  const total = results.positive + results.negative;
  ["positive", "negative"].forEach((type) => {
    const value = results[type];
    const barEl = document.getElementById(`results-bar-${type}`);
    const countEl = document.getElementById(`results-count-${type}`);

    barEl.style = `width: ${(value / total) * 100}%`;
    countEl.textContent = value;
  });
}
