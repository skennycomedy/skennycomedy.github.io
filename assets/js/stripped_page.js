"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import ChatWidget from "@/components/ChatWidget";

export default function Home() {
  const [pages, setPages] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/wp-json/wp/v2/posts")
      .then((res) => setPages(res.data))
      .catch((err) => console.error("Error fetching pages:", err));
  }, []);

  return (
    <div style={{ fontFamily: "Arial, sans-serif", margin: 20 }}>
      <div style={{ marginBottom: 40 }}>
        {pages.length ? (
          pages.map(({ id, title }) => (
            <div
              key={id}
              style={{
                border: "1px solid #ddd",
                padding: 15,
                borderRadius: 8,
                marginBottom: 15,
              }}
            >
              <h2>{title.rendered}</h2>
              <div />
            </div>
          ))
        ) : (
          <p style={{ textAlign: "center", color: "#999" }}>
            Loading WordPress content...
          </p>
        )}
      </div>
      {/* Chat Widget */}
      <div className="chat-widget">
        <ChatWidget />
      </div>

    </div>
  );
}
