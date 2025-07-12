async function sendMessage() {
    const input = document.getElementById("user-input").value;
    const language = document.getElementById("language").value;
    const output = document.getElementById("chat-output");

    if (!input) return;

    output.innerHTML += `<p><strong>You:</strong> ${input}</p>`;
    
    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input, language })
    }).then(res => res.json());

    output.innerHTML += `<p><strong>Bot:</strong> ${response.response} ${response.cached ? "(Cached)" : ""}</p>`;
    output.scrollTop = output.scrollHeight;
    document.getElementById("user-input").value = "";
}