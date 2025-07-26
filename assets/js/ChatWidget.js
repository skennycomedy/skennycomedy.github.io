"use client";

import React, { useState } from "react";

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", message: input };
    setMessages([...messages, { sender: "user", text: input }]);
    setInput("");

    try {
      const response = await fetch("http://localhost:5005/webhooks/rest/webhook", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userMessage),
      });

      const data = await response.json();
      const botReplies = data.map((msg) => ({
        sender: "bot",
        text: msg.text || "[no response]",
      }));

      setMessages((prev) => [...prev, ...botReplies]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "[Error connecting to bot]" },
      ]);
    }
  };

  return (
    <div style={styles.wrapper}>
      {isOpen ? (
        <div style={styles.container}>
          <div style={styles.header}>
            <strong>Chat</strong>
            <button onClick={() => setIsOpen(false)} style={styles.closeButton}>
              ×
            </button>
          </div>
          <div style={styles.chatBox}>
            {messages.map((msg, i) => (
              <div
                key={i}
                style={{
                  ...styles.message,
                  alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
                  backgroundColor: msg.sender === "user" ? "#cce5ff" : "#f1f1f1",
                }}
              >
                {msg.text}
              </div>
            ))}
          </div>
          <div style={styles.inputArea}>
            <input
              style={styles.input}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            />
            <button style={styles.button} onClick={sendMessage}>
              Send
            </button>
          </div>
        </div>
      ) : (
        <button style={styles.floatingButton} onClick={() => setIsOpen(true)}>
          💬
        </button>
      )}
    </div>
  );
}

const styles = {
  wrapper: {
    position: "fixed",
    bottom: "20px",
    right: "20px",
    zIndex: 9999,
  },
  container: {
    width: "350px",
    border: "1px solid #ccc",
    borderRadius: "8px",
    backgroundColor: "#ffffff",
    boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
    display: "flex",
    flexDirection: "column",
    fontFamily: "Arial, sans-serif",
  },
  header: {
    padding: "0.5rem 1rem",
    borderBottom: "1px solid #ddd",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "#f5f5f5",
    borderTopLeftRadius: "8px",
    borderTopRightRadius: "8px",
  },
  closeButton: {
    background: "transparent",
    border: "none",
    fontSize: "1.2rem",
    cursor: "pointer",
  },
  chatBox: {
    display: "flex",
    flexDirection: "column",
    gap: "0.5rem",
    height: "250px",
    overflowY: "auto",
    padding: "0.5rem 1rem",
    backgroundColor: "#fafafa",
  },
  message: {
    padding: "0.5rem 0.75rem",
    borderRadius: "12px",
    maxWidth: "80%",
    fontSize: "15px",
    lineHeight: "1.5",
    color: "#222222",
  },
  inputArea: {
    display: "flex",
    gap: "0.5rem",
    padding: "0.5rem 1rem 1rem",
  },
  input: {
    flex: 1,
    padding: "0.5rem",
    borderRadius: "4px",
    border: "1px solid #bbb",
    backgroundColor: "#ffffff",
    color: "#222222",
    fontSize: "14px",
  },
  button: {
    padding: "0.5rem 1rem",
    border: "none",
    backgroundColor: "#007bff",
    color: "#fff",
    borderRadius: "4px",
    cursor: "pointer",
  },
  floatingButton: {
    backgroundColor: "#007bff",
    color: "#fff",
    border: "none",
    borderRadius: "50%",
    width: "48px",
    height: "48px",
    fontSize: "20px",
    cursor: "pointer",
    boxShadow: "0 4px 8px rgba(0,0,0,0.2)",
  },
};
