import React, { useState } from 'react';
import ChatBox from './ChatBox';
import './SmartieWidget.css';

function SmartieWidget() {
  const [open, setOpen] = useState(false);

  return (
    <div className="smartie-widget">
      {open && <ChatBox />}
      <button className="chat-toggle-button" onClick={() => setOpen(!open)}>
        💬 Smartie
      </button>
    </div>
  );
}

export default SmartieWidget;
