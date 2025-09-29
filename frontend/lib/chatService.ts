export interface Source {
  title: string
  url: string
  snippet: string
  type: 'web' | 'arxiv' | 'youtube'
  published_date?: string
  score: number
  // YouTube-specific fields
  duration?: string
  channel?: string
  thumbnail?: string
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  metadata?: {
    tools_used?: string[]
    processing_time?: number
    helpfulness_score?: number
    search_results_count?: number
    sources?: Source[]
  }
}

export interface ChatResponse {
  response: string
  session_id: string
  metadata: {
    tools_used?: string[]
    processing_time?: number
    helpfulness_score?: number
    search_results_count?: number
    sources?: Source[]
  }
  timestamp: Date
}

export interface HealthResponse {
  status: string
  timestamp: Date
  agent_ready: boolean
  api_keys_configured: boolean
}

export class ChatService {
  private baseUrl: string
  private openaiApiKey: string = ''
  private tavilyApiKey: string = ''

  constructor() {
    // Debug logging
    const isDevelopment = process.env.NODE_ENV === 'development'
    console.log('🔧 ChatService Debug Info:')
    console.log('NODE_ENV:', process.env.NODE_ENV)
    console.log('isDevelopment:', isDevelopment)
    console.log('NEXT_PUBLIC_BACKEND_URL:', process.env.NEXT_PUBLIC_BACKEND_URL)
    console.log('NEXT_PUBLIC_RAILWAY_URL:', process.env.NEXT_PUBLIC_RAILWAY_URL)
    
    if (isDevelopment) {
      // Local development
      this.baseUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'
      console.log('🏠 Using LOCAL backend:', this.baseUrl)
    } else {
      // Production: Vercel frontend + Railway backend
      this.baseUrl = process.env.NEXT_PUBLIC_RAILWAY_URL || 'https://langgraph-ai-agent-production-561e.up.railway.app'
      console.log('🚀 Using PRODUCTION backend:', this.baseUrl)
    }
  }

  setApiKeys(openaiKey: string, tavilyKey: string) {
    this.openaiApiKey = openaiKey
    this.tavilyApiKey = tavilyKey
  }

  async healthCheck(): Promise<HealthResponse> {
    console.log('🔍 Health check attempting to connect to:', this.baseUrl + '/health')
    try {
      const response = await fetch(`${this.baseUrl}/health`, {
        method: 'GET',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      
      console.log('📡 Health check response status:', response.status)
      console.log('📡 Health check response headers:', Object.fromEntries(response.headers.entries()))
      
      if (!response.ok) {
        throw new Error(`Health check failed: ${response.status} ${response.statusText}`)
      }
      
      const data = await response.json()
      console.log('✅ Health check success:', data)
      return data
    } catch (error) {
      console.error('❌ Health check error:', error)
      throw new Error(`Backend connection failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  async sendMessage(message: string, sessionId: string): Promise<ChatResponse> {
    const response = await fetch(`${this.baseUrl}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        session_id: sessionId,
        openai_api_key: this.openaiApiKey,
        tavily_api_key: this.tavilyApiKey,
      }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to send message')
    }

    const data = await response.json()
    return {
      ...data,
      timestamp: new Date(data.timestamp),
    }
  }

  async *sendMessageStream(message: string, sessionId: string): AsyncGenerator<{
    type: 'start' | 'chunk' | 'done' | 'error'
    content?: string
    full_content?: string
    metadata?: any
    session_id?: string
    error?: string
  }> {
    const response = await fetch(`${this.baseUrl}/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        session_id: sessionId,
        openai_api_key: this.openaiApiKey,
        tavily_api_key: this.tavilyApiKey,
      }),
    })

    if (!response.ok) {
      throw new Error('Failed to start streaming')
    }

    const reader = response.body?.getReader()
    const decoder = new TextDecoder()

    if (!reader) {
      throw new Error('No response body')
    }

    try {
      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              yield data
            } catch (e) {
              console.error('Failed to parse SSE data:', e)
            }
          }
        }
      }
    } finally {
      reader.releaseLock()
    }
  }

  async getChatHistory(sessionId: string): Promise<ChatMessage[]> {
    const response = await fetch(`${this.baseUrl}/chat/${sessionId}/history`)
    if (!response.ok) {
      throw new Error('Failed to get chat history')
    }
    const data = await response.json()
    return data.map((msg: any) => ({
      ...msg,
      timestamp: new Date(msg.timestamp),
    }))
  }

  async clearHistory(sessionId: string): Promise<void> {
    const response = await fetch(`${this.baseUrl}/chat/${sessionId}`, {
      method: 'DELETE',
    })
    if (!response.ok) {
      throw new Error('Failed to clear chat history')
    }
  }

  async getSessions(): Promise<{ sessions: string[]; total_sessions: number }> {
    const response = await fetch(`${this.baseUrl}/sessions`)
    if (!response.ok) {
      throw new Error('Failed to get sessions')
    }
    return response.json()
  }
}