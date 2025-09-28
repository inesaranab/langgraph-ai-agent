'use client'

import { useState, useRef, useEffect } from 'react'
import { ChatMessage } from '../lib/chatService'
import MessageBubble from './MessageBubble'
import MessageInput from './MessageInput'

interface ChatInterfaceProps {
  messages: ChatMessage[]
  isLoading: boolean
  onSendMessage: (message: string) => void
  isConnected: boolean
  disabled?: boolean
}

export default function ChatInterface({ 
  messages, 
  isLoading, 
  onSendMessage, 
  isConnected,
  disabled = false
}: ChatInterfaceProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  return (
    <div className="flex-1 flex flex-col min-h-0">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4 scroll-mt-20">
        {messages.length === 0 ? (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center max-w-md">
              <div className="w-16 h-16 bg-gradient-to-r from-primary-600 to-primary-700 rounded-full flex items-center justify-center mb-6">
                <div className="w-8 h-8 bg-dark-50 rounded-full"></div>
              </div>
              <h2 className="text-2xl font-bold text-dark-800 mb-2">
                Welcome to Research AI Agent
              </h2>
              
              {disabled ? (
                <div className="mb-6">
                  <p className="text-dark-600 mb-4">
                    Configure your API keys to start using the AI assistant.
                  </p>
                  <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-sm text-yellow-800">
                    <p className="font-medium mb-2">⚙️ Click the Settings button in the header to:</p>
                    <ul className="text-left space-y-1 ml-4">
                      <li>• Add your OpenAI API key</li>
                      <li>• Add your Tavily API key</li>
                      <li>• Start chatting with the AI</li>
                    </ul>
                  </div>
                </div>
              ) : (
                <>
                  <p className="text-dark-600 mb-6">
                    An intelligent agent powered by LangGraph. Get help with web search, 
                    research academic papers, and complex questions with real-time information.
                  </p>
                  <div className="bg-dark-100 border border-primary-200 rounded-lg p-4 text-sm text-dark-700">
                    <p className="font-medium mb-3 text-primary-700">Available capabilities:</p>
                    <ul className="text-left space-y-2">
                      <li className="flex items-center space-x-2">
                        <div className="w-1.5 h-1.5 bg-primary-500 rounded-full"></div>
                        <span>Web search for current information</span>
                      </li>
                      <li className="flex items-center space-x-2">
                        <div className="w-1.5 h-1.5 bg-primary-500 rounded-full"></div>
                        <span>Academic research via ArXiv</span>
                      </li>
                      <li className="flex items-center space-x-2">
                        <div className="w-1.5 h-1.5 bg-primary-500 rounded-full"></div>
                        <span>General questions and analysis</span>
                      </li>
                      <li className="flex items-center space-x-2">
                        <div className="w-1.5 h-1.5 bg-primary-500 rounded-full"></div>
                        <span>Multi-step reasoning tasks</span>
                      </li>
                    </ul>
                  </div>
                </>
              )}
            </div>
          </div>
        ) : (
          <div className="max-w-4xl mx-auto space-y-4">
            {messages.map((message, index) => (
              <MessageBubble key={index} message={message} />
            ))}
            {isLoading && (
              <div className="flex items-center space-x-3 text-dark-500">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                  <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                </div>
                <span className="text-sm">Processing request...</span>
              </div>
            )}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-dark-200 bg-dark-100 px-6 py-4 scroll-mt-20">
        <div className="max-w-4xl mx-auto">
          <MessageInput 
            onSendMessage={onSendMessage} 
            isLoading={isLoading}
            isConnected={isConnected && !disabled}
            disabled={disabled}
          />
        </div>
      </div>
    </div>
  )
}