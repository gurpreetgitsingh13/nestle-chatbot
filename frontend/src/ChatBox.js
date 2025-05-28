import React, { useState } from "react";

function ChatBox() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSend = async () => {
    const userMsg = { sender: "user", text: query };
    setMessages((prev) => [...prev, userMsg]);

    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query, top_k: 3 }),
    });

    const data = await response.json();
    const botMsg = {
      sender: "bot",
      text: data.results
        .map(
          (r) => `• **${r.title}**\n[${r.url}](${r.url})\n${r.snippet}`
        )
        .join("\n\n"),
    };

    setMessages((prev) => [...prev, botMsg]);
    setQuery("");
  };

  return (
    <div style={{ padding: 20 }}>
      <div
        style={{ maxHeight: 400, overflowY: "scroll", marginBottom: 10 }}
      >
        {messages.map((m, idx) => (
          <div
            key={idx}
            style={{
              margin: "10px 0",
              textAlign: m.sender === "user" ? "right" : "left",
              whiteSpace: "pre-wrap",
            }}
          >
            <b>{m.sender === "user" ? "You" : "Nestlé AI"}:</b>
            <div
              dangerouslySetInnerHTML={{
                __html: m.text.replace(/\n/g, "<br/>")
              }}
            />
          </div>
        ))}
      </div>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ width: "80%" }}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}

export default ChatBox;
