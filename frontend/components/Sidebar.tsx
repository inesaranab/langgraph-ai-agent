'use client'

interface SidebarProps {
  sessionId: string
  isConnected: boolean
  onClearChat: () => void
  onNewSession: () => void
  onRefreshConnection: () => void
}

export default function Sidebar({ 
  sessionId, 
  isConnected, 
  onClearChat, 
  onNewSession, 
  onRefreshConnection 
}: SidebarProps) {
  return (
    <div className="w-80 sidebar flex flex-col">
      {/* Header */}
      <div className="p-6 border-b border-dark-200">
        <h2 className="text-lg font-semibold text-dark-800">Chat Session</h2>
        <p className="text-sm text-dark-600 mt-1">
          ID: {sessionId.substring(0, 8)}...
        </p>
      </div>

      {/* Connection Status */}
      <div className="p-4 border-b border-dark-200">
        <div className={`p-3 rounded-lg ${
          isConnected 
            ? 'bg-primary-50 border border-primary-200' 
            : 'bg-red-50 border border-red-200'
        }`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${
                isConnected ? 'bg-primary-500' : 'bg-red-500'
              }`} />
              <span className={`text-sm font-medium ${
                isConnected ? 'text-primary-800' : 'text-red-800'
              }`}>
                {isConnected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
            <button
              onClick={onRefreshConnection}
              className="text-xs text-dark-500 hover:text-dark-700"
            >
              Refresh
            </button>
          </div>
          
          {!isConnected && (
            <p className="text-xs text-red-600 mt-1">
              Make sure the backend server is running on port 8000
            </p>
          )}
        </div>
      </div>

      {/* Actions */}
      <div className="p-4 space-y-3">
        <button
          onClick={onNewSession}
          className="w-full button-primary text-sm"
        >
          New Session
        </button>
        
        <button
          onClick={onClearChat}
          className="w-full button-secondary text-sm"
        >
          Clear Chat
        </button>
      </div>

      {/* Agent Information */}
      <div className="p-4 border-t border-dark-200 mt-auto">
        <h3 className="text-sm font-medium text-dark-800 mb-3">Available Tools</h3>
        <div className="space-y-2 text-sm text-dark-600">
          <div className="flex items-center space-x-3">
            <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
            <span>Web Search (Tavily)</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
            <span>ArXiv Research</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
            <span>Youtube Search</span>
          </div>
        </div>
        
        <div className="mt-4 pt-3 border-t border-dark-200">
          <p className="text-xs text-dark-500">
            Powered by LangGraph & Next.js
          </p>
        </div>
      </div>
    </div>
  )
}