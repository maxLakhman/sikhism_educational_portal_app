document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("ask-form");
  const promptInput = document.getElementById("prompt");
  const responseDisplay = document.getElementById("response");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    const prompt = promptInput.value.trim();
    if (!prompt) return;

    responseDisplay.textContent = "Thinking...\n";
    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let result = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      result += decoder.decode(value, { stream: true });
      responseDisplay.textContent = result;
    }
  });
});
// This script handles the form submission and updates the response display in real-time.
// It uses the Fetch API to send the prompt to the server and reads the response stream.
