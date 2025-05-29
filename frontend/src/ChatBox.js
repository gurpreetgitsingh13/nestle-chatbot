import React, { useState } from 'react';
import './ChatBox.css';

function ChatBox() {
  const [query, setQuery] = useState('');
  const [chatLog, setChatLog] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!query.trim()) return;
    const userMessage = { sender: 'You', message: query };
    setChatLog(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, top_k: 3 })
      });

      const data = await response.json();
      let botMessage;

      if (data.results?.length > 0) {
        botMessage = {
          sender: 'Smartie',
          message: data.results.map(r => ({ snippet: r.snippet }))
        };
      } else {
        botMessage = {
          sender: 'Smartie',
          message: data.message || "Sorry, I couldn't find anything relevant."
        };
      }

      setChatLog(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      setChatLog(prev => [...prev, {
        sender: 'Smartie',
        message: 'An error occurred. Please try again later.'
      }]);
    }

    setLoading(false);
    setQuery('');
  };

  return (
    <div className="chatbox-container">
      <div className="chat-log">
        {chatLog.map((entry, idx) => (
          <div key={idx} className={`chat-entry ${entry.sender === 'You' ? 'user' : 'bot'}`}>
            <strong>{entry.sender}:</strong>
            {Array.isArray(entry.message) ? (
              entry.message.map((item, i) => (
                <div key={i} className="result-card">
                  <p>{item.snippet}</p>
                </div>
              ))
            ) : (
              <p>{entry.message}</p>
            )}
          </div>
        ))}
        {loading && <div className="chat-entry bot">Smartie: <i>Typing...</i></div>}
      </div>

      <div className="input-container">
        <input
          type="text"
          placeholder="Ask me about recipes, ingredients..."
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}

export default ChatBox;
