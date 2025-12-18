import React, { useState, useRef, useEffect } from 'react';
import { chatAPI } from './services/api';
import ChatMessage from './components/ChatMessage';
import FileUpload from './components/FileUpload';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [model, setModel] = useState('gemini-1.5-pro');
  const [temperature, setTemperature] = useState(0.7);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { role: 'user', content: input.trim() };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      const response = await chatAPI.sendMessage(newMessages, model, temperature);
      const assistantMessage = {
        role: 'assistant',
        content: response.response,
        toolCalls: response.tool_calls,
      };
      setMessages([...newMessages, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        role: 'assistant',
        content: `Error: ${error.response?.data?.detail || error.message || 'No se pudo procesar la solicitud'}`,
      };
      setMessages([...newMessages, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleUploadSuccess = (result) => {
    const uploadMessage = {
      role: 'assistant',
      content: `✅ ${result.message}\n\nColumnas: ${result.data_summary.columns.join(', ')}\nFilas: ${result.data_summary.row_count}\n\n¿Qué análisis te gustaría realizar?`,
    };
    setMessages([...messages, uploadMessage]);
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>💰 Asistente Analista Financiero</h1>
        <p className="subtitle">Powered by Vertex AI Gemini</p>
      </header>

      <div className="controls">
        <div className="control-group">
          <label>Modelo:</label>
          <select value={model} onChange={(e) => setModel(e.target.value)}>
            <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
            <option value="gemini-1.5-flash">Gemini 1.5 Flash</option>
            <option value="gemini-pro">Gemini Pro</option>
          </select>
        </div>

        <div className="control-group">
          <label>Temperatura: {temperature.toFixed(1)}</label>
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={temperature}
            onChange={(e) => setTemperature(parseFloat(e.target.value))}
          />
        </div>

        <FileUpload onUploadSuccess={handleUploadSuccess} />

        <button onClick={clearChat} className="clear-button">
          🗑️ Limpiar
        </button>
      </div>

      <div className="chat-container">
        <div className="messages">
          {messages.length === 0 && (
            <div className="welcome-message">
              <h2>¡Bienvenido!</h2>
              <p>Soy tu asistente de análisis financiero. Puedo ayudarte con:</p>
              <ul>
                <li>📊 Análisis de estados financieros</li>
                <li>📈 Cálculo de ratios financieros (liquidez, endeudamiento, rentabilidad)</li>
                <li>📉 Análisis de tendencias</li>
                <li>💹 Proyecciones de flujo de caja (DCF)</li>
                <li>⚠️ Identificación de riesgos financieros</li>
              </ul>
              <p>Carga un archivo CSV con tus datos o hazme una pregunta.</p>
            </div>
          )}
          {messages.map((msg, idx) => (
            <ChatMessage
              key={idx}
              message={msg}
              toolCalls={msg.toolCalls}
            />
          ))}
          {loading && (
            <div className="loading-indicator">
              <div className="spinner"></div>
              <span>Pensando...</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-area">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Escribe tu pregunta o solicitud de análisis..."
            disabled={loading}
            rows="3"
          />
          <button onClick={handleSend} disabled={loading || !input.trim()}>
            {loading ? '⏳' : '📤'} Enviar
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
