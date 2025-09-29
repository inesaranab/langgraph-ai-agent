'use client'

import { useState, useEffect, useRef } from 'react'
import ChatInterface from '../components/ChatInterface'
import Sidebar from '../components/Sidebar'
import SettingsModal from '../components/SettingsModal'
import SourcesPanel from '../components/SourcesPanel'
import { ChatMessage, ChatService, Source } from '../lib/chatService'
import { Settings, AlertTriangle, FileSearch } from 'lucide-react'

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState<string>('')
  const [isConnected, setIsConnected] = useState(false)
  const [apiKeys, setApiKeys] = useState<{ openai: string; tavily: string }>({ openai: '', tavily: '' })
  const [hasValidApiKeys, setHasValidApiKeys] = useState(false)
  const [isSettingsOpen, setIsSettingsOpen] = useState(false)
  const [isSourcesPanelOpen, setIsSourcesPanelOpen] = useState(false)
  const [allSources, setAllSources] = useState<Source[]>([])
  const chatService = useRef(new ChatService())

  useEffect(() => {
    // Generate session ID
    setSessionId(Math.random().toString(36).substring(7))
    
    // Check backend connection
    checkConnection()
  }, [])

  const checkConnection = async () => {
    try {
      const health = await chatService.current.healthCheck()
      // Connection is successful if health check passes (accept both v1 and v2 formats)
      setIsConnected(health.status === 'healthy' || health.status === 'healthy-v2')
    } catch (error) {
      setIsConnected(false)
    }
  }

  const handleApiKeysChange = (keys: { openai: string; tavily: string }) => {
    setApiKeys(keys)
    setHasValidApiKeys(keys.openai.trim() !== '' && keys.tavily.trim() !== '')
    
    // Update chat service with new API keys
    chatService.current.setApiKeys(keys.openai, keys.tavily)
  }

  const handleSendMessage = async (message: string) => {
    if (!message.trim() || isLoading) return

    // Add user message
    const userMessage: ChatMessage = {
      role: 'user',
      content: message,
      timestamp: new Date(),
    }
    
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    // Create placeholder for streaming response
    const assistantMessageId = Date.now().toString()
    const assistantMessage: ChatMessage = {
      role: 'assistant',
      content: '',
      timestamp: new Date(),
    }
    
    setMessages(prev => [...prev, assistantMessage])

    try {
      let fullContent = ''
      let finalMetadata = {}
      
      // Use streaming API
      const stream = chatService.current.sendMessageStream(message, sessionId)
      
      for await (const chunk of stream) {
        if (chunk.type === 'chunk' && chunk.full_content) {
          fullContent = chunk.full_content
          
          // Update the message in real-time
          setMessages(prev => prev.map((msg, index) => 
            index === prev.length - 1 && msg.role === 'assistant' 
              ? { ...msg, content: fullContent }
              : msg
          ))
        } else if (chunk.type === 'done') {
          finalMetadata = chunk.metadata || {}
          
          // Final update with metadata
          setMessages(prev => prev.map((msg, index) => 
            index === prev.length - 1 && msg.role === 'assistant' 
              ? { ...msg, content: fullContent, metadata: finalMetadata }
              : msg
          ))
          
          // Add sources to collection if they exist
          const sources = (finalMetadata as any)?.sources as Source[]
          if (sources && Array.isArray(sources) && sources.length > 0) {
            setAllSources(prev => [...prev, ...sources])
          }
        } else if (chunk.type === 'error') {
          throw new Error(chunk.error || 'Streaming error')
        }
      }
      
    } catch (error) {
      // Replace the assistant message with error
      setMessages(prev => prev.map((msg, index) => 
        index === prev.length - 1 && msg.role === 'assistant' 
          ? { ...msg, content: 'Sorry, I encountered an error. Please try again.' }
          : msg
      ))
      console.error('Chat error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleClearChat = async () => {
    try {
      await chatService.current.clearHistory(sessionId)
      setMessages([])
      setAllSources([])
    } catch (error) {
      console.error('Error clearing chat:', error)
    }
  }

  const handleNewSession = () => {
    setSessionId(Math.random().toString(36).substring(7))
    setMessages([])
    setAllSources([])
  }

  return (
    <div className="flex h-screen bg-dark-50">
      <Sidebar
        sessionId={sessionId}
        isConnected={isConnected}
        onClearChat={handleClearChat}
        onNewSession={handleNewSession}
        onRefreshConnection={checkConnection}
      />
      
      <div className="flex-1 flex flex-col">
        <header className="sticky top-0 z-10 bg-dark-100 shadow-sm border-b border-dark-200 px-6 py-4 h-16">
          <div className="flex items-center justify-between h-full">
            <div>
              <h1 className="text-xl font-bold text-dark-800">Research AI Agent</h1>
              <p className="text-xs text-dark-600">Intelligent AI agent powered by LangGraph</p>
            </div>
            
            <div className="flex items-center space-x-4">
              {!hasValidApiKeys && (
                <div className="flex items-center space-x-2 px-3 py-1 rounded-full text-sm bg-red-100 text-red-800">
                  <AlertTriangle className="w-3 h-3" />
                  <span>API Keys Required</span>
                </div>
              )}
              
              <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm ${
                isConnected 
                  ? 'bg-primary-100 text-primary-800' 
                  : 'bg-red-100 text-red-800'
              }`}>
                <div className={`w-2 h-2 rounded-full ${
                  isConnected ? 'bg-primary-500' : 'bg-red-500'
                }`} />
                <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
              </div>
              
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setIsSourcesPanelOpen(true)}
                  className="relative p-2 rounded-lg hover:bg-dark-200 text-dark-600 hover:text-dark-800 transition-colors"
                  title={`View Sources (${allSources.length})`}
                >
                  <FileSearch className="w-5 h-5" />
                  {allSources.length > 0 && (
                    <span className="absolute -top-1 -right-1 bg-primary-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                      {allSources.length > 9 ? '9+' : allSources.length}
                    </span>
                  )}
                </button>
                
                <button
                  onClick={() => setIsSettingsOpen(true)}
                  className="p-2 rounded-lg hover:bg-dark-200 text-dark-600 hover:text-dark-800 transition-colors"
                  title="Settings"
                >
                  <Settings className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        </header>

        <div className="flex-1 flex flex-col min-h-0">
          <ChatInterface
            messages={messages}
            isLoading={isLoading}
            onSendMessage={handleSendMessage}
            isConnected={isConnected && hasValidApiKeys}
            disabled={!hasValidApiKeys}
          />
        </div>
      </div>

      {/* Settings Modal */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        onApiKeysChange={handleApiKeysChange}
      />

      {/* Sources Panel */}
      <SourcesPanel
        isOpen={isSourcesPanelOpen}
        onClose={() => setIsSourcesPanelOpen(false)}
        allSources={allSources}
      />
    </div>
  )
}