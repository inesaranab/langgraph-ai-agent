export interface Source {
  title: string
  url: string
  snippet: string
  type: 'web' | 'arxiv'
  published_date?: string
  score: number
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
    // Configure for Railway backend deployment
    const isDevelopment = process.env.NODE_ENV === 'development'
    
    if (isDevelopment) {
      // Local development - use local backend
      this.baseUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'
    } else {
      // Production - use Railway backend URL
      this.baseUrl = process.env.NEXT_PUBLIC_RAILWAY_URL || 'https://your-app-name.railway.app'
    }
    
    console.log('ChatService configured for:', this.baseUrl)
  }

  setApiKeys(openaiKey: string, tavilyKey: string) {
    this.openaiApiKey = openaiKey
    this.tavilyApiKey = tavilyKey
  }

  async healthCheck(): Promise<HealthResponse> {
    const response = await fetch(`${this.baseUrl}/health`)
    if (!response.ok) {
      throw new Error('Health check failed')
    }
    return response.json()
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