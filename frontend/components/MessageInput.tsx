'use client'

import { useState } from 'react'

interface MessageInputProps {
  onSendMessage: (message: string) => void
  isLoading: boolean
  isConnected: boolean
  disabled?: boolean
}

export default function MessageInput({ 
  onSendMessage, 
  isLoading, 
  isConnected,
  disabled = false
}: MessageInputProps) {
  const [message, setMessage] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (message.trim() && !isLoading && isConnected && !disabled) {
      onSendMessage(message.trim())
      setMessage('')
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex space-x-4">
      <div className="flex-1">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={
            disabled
              ? "Please configure your API keys above..."
              : !isConnected 
              ? "Please check your backend connection..." 
              : "Ask me anything..."
          }
          disabled={isLoading || !isConnected || disabled}
          rows={1}
          className="w-full px-4 py-3 bg-dark-100 border border-dark-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none disabled:bg-dark-200 disabled:cursor-not-allowed text-dark-800 placeholder-dark-500"
          style={{ minHeight: '52px', maxHeight: '120px' }}
        />
      </div>
      
      <button
        type="submit"
        disabled={!message.trim() || isLoading || !isConnected || disabled}
        className="button-primary disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLoading ? (
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            <span>Sending...</span>
          </div>
        ) : (
          <span>Send</span>
        )}
      </button>
    </form>
  )
}