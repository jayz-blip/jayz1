import React, { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: '안녕하세요! 👋 사내용 채팅 AI입니다. 무엇을 도와드릴까요?',
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || loading) return

    const userMessage = {
      role: 'user',
      content: input,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      // Cloudflare Pages Functions 프록시 사용
      // /api/chat으로 요청하면 functions/api/[[path]].js가 Workers로 프록시
      // 프로덕션에서는 /api 사용, 로컬 개발 시에만 VITE_API_URL 사용
      const API_URL = import.meta.env.VITE_API_URL || '/api';
      const isLocalDev = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      const finalApiUrl = isLocalDev && import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : '/api';
      
      console.log('🔗 API URL:', finalApiUrl);
      console.log('📤 전송할 질문:', input);
      
      const response = await axios.post(`${finalApiUrl}/chat`, {
        message: input
      })
      
      console.log('📥 서버 응답:', response.data);
      console.log('✅ 응답 성공');

      const assistantMessage = {
        role: 'assistant',
        content: response.data.response,
        sources: response.data.sources,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('❌ 오류 발생!');
      console.error('오류 객체:', error);
      console.error('오류 메시지:', error.message);
      if (error.response) {
        console.error('서버 응답 상태:', error.response.status);
        console.error('서버 응답 데이터:', error.response.data);
      }
      if (error.request) {
        console.error('요청은 보냈지만 응답을 받지 못함:', error.request);
      }
      
      const errorMessage = {
        role: 'assistant',
        content: `오류가 발생했습니다: ${error.message || '알 수 없는 오류'}. CMD 창과 브라우저 콘솔을 확인해주세요. 😢`,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="app">
      <div className="chat-container">
        <div className="chat-header">
          <div className="header-content">
            <span className="header-emoji">🤖</span>
            <h1>사내용 채팅 AI</h1>
            <span className="status-dot"></span>
          </div>
        </div>

        <div className="messages-container">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="message-content">
                {msg.role === 'assistant' && (
                  <div className="avatar">🤖</div>
                )}
                <div className="message-bubble">
                  <p>{msg.content}</p>
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="sources">
                      <small>📚 참고 자료 {msg.sources.length}개</small>
                    </div>
                  )}
                </div>
                {msg.role === 'user' && (
                  <div className="avatar user">👤</div>
                )}
              </div>
            </div>
          ))}
          {loading && (
            <div className="message assistant">
              <div className="message-content">
                <div className="avatar">🤖</div>
                <div className="message-bubble loading">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-container">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="메시지를 입력하세요... 💬"
            rows={1}
            disabled={loading}
          />
          <button 
            onClick={handleSend} 
            disabled={loading || !input.trim()}
            className="send-button"
          >
            {loading ? '⏳' : '🚀'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default App

