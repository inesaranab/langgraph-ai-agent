'use client'

import { ChatMessage } from '../lib/chatService'
import MarkdownRenderer from './MarkdownRenderer'
import SourceCitation from './SourceCitation'

interface MessageBubbleProps {
  message: ChatMessage
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user'
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-3xl rounded-lg px-6 py-4 ${
        isUser 
          ? 'user-message' 
          : 'assistant-message'
      }`}>
        {isUser ? (
          <div className="whitespace-pre-wrap break-words">
            {message.content}
          </div>
        ) : (
          <>
            <MarkdownRenderer 
              content={message.content}
              className="max-w-none"
            />
            
            {/* Sources Citation */}
            {message.metadata?.sources && message.metadata.sources.length > 0 && (
              <SourceCitation sources={message.metadata.sources} />
            )}
          </>
        )}
        
        {/* Metadata for assistant messages */}
        {!isUser && message.metadata && (
          <div className="mt-4 pt-3 border-t border-dark-200 text-xs text-dark-500">
            <div className="flex flex-wrap gap-4">
              {message.metadata.tools_used && message.metadata.tools_used.length > 0 && (
                <div className="flex items-center space-x-2">
                  <span className="font-medium text-primary-600">Tools:</span>
                  <span>{message.metadata.tools_used.join(', ')}</span>
                </div>
              )}
              
              {message.metadata.processing_time && (
                <div className="flex items-center space-x-2">
                  <span className="font-medium text-primary-600">Time:</span>
                  <span>{message.metadata.processing_time.toFixed(2)}s</span>
                </div>
              )}
              
              {message.metadata.helpfulness_score && (
                <div className="flex items-center space-x-2">
                  <span className="font-medium text-primary-600">Quality:</span>
                  <span>{(message.metadata.helpfulness_score * 100).toFixed(0)}%</span>
                </div>
              )}

              {message.metadata.sources && message.metadata.sources.length > 0 && (
                <div className="flex items-center space-x-2">
                  <span className="font-medium text-primary-600">Sources:</span>
                  <span>{message.metadata.sources.length} found</span>
                </div>
              )}
              

            </div>
          </div>
        )}
        
        <div className={`text-xs mt-2 ${isUser ? 'text-primary-100' : 'text-dark-400'}`}>
          {message.timestamp.toLocaleTimeString()}
        </div>
      </div>
    </div>
  )
}