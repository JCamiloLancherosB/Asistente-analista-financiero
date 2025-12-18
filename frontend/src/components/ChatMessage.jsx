import React from 'react';
import './ChatMessage.css';

function ChatMessage({ message, toolCalls }) {
  const isUser = message.role === 'user';

  return (
    <div className={`message ${isUser ? 'user-message' : 'assistant-message'}`}>
      <div className="message-header">
        <strong>{isUser ? '👤 Usuario' : '🤖 Asistente'}</strong>
      </div>
      <div className="message-content">
        {message.content}
      </div>
      {toolCalls && toolCalls.length > 0 && (
        <div className="tool-calls">
          <div className="tool-calls-header">🔧 Herramientas utilizadas:</div>
          {toolCalls.map((call, idx) => (
            <div key={idx} className="tool-call">
              <strong>{call.name}</strong>
              {call.arguments && (
                <pre>{JSON.stringify(call.arguments, null, 2)}</pre>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ChatMessage;
