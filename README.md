# LangGraph AI Agent 🤖

A production-ready AI agent application built with **LangGraph**, featuring a modern ReacVisit: http://localhost:3000

## 🎬 YouTube Integration

The app automatically searches for educational YouTube videos related to your queries! 

**Features:**
- **No API Key Required**: Uses the `youtube-search` library
- **Educational Focus**: Finds tutorials, explanations, and learning resources
- **Rich Metadata**: Displays video duration, channel, and thumbnails
- **Visual Design**: Red-themed YouTube sources with Play button icons
- **Smart Integration**: Automatically triggered for learning-related questions

**Example queries that trigger YouTube search:**
- "How do I learn Python programming?"
- "Explain machine learning concepts"
- "React tutorial for beginners"
- "JavaScript fundamentals"

The YouTube videos appear in the **Sources panel** with a distinctive red theme and can be filtered separately from web and academic sources.

## 🌍 Environment Variablesntend and FastAPI backend with full tool integration.

## ✨ Features

- **🧠 Advanced LangGraph Agent**: Intelligent workflow with conditional tool routing
- **🌐 Web Search Integration**: Real-time information via Tavily API
- **📚 Academic Search**: ArXiv paper search and analysis
- **🎬 Educational Videos**: YouTube search integration for learning resources
- **📊 Quality Control**: Built-in helpfulness evaluation
- **💬 Modern Chat UI**: React + Next.js with streaming responses
- **🎨 Beautiful Design**: Black & gold themed interface with color-coded sources
- **📱 Responsive**: Works on desktop and mobile
- **🔒 Secure**: User-provided API keys (no server-side key storage)

## 🚀 Live Demo

- **Frontend**: https://myfirstadvanced-ipvmmodlp-inesaranabs-projects.vercel.app
- **Backend API**: https://langgraph-ai-agent-production-561e.up.railway.app
- **API Docs**: https://langgraph-ai-agent-production-561e.up.railway.app/docs

## 🏗️ Architecture

```
┌─────────────────┐    HTTPS/WSS    ┌──────────────────┐
│   Vercel        │ ──────────────► │   Railway        │
│   Frontend      │                 │   Backend        │
│   - Next.js     │ ◄────────────── │   - FastAPI      │
│   - React       │    JSON/SSE     │   - LangGraph    │
│   - TypeScript  │                 │   - AI Tools     │
└─────────────────┘                 └──────────────────┘
```

## 🛠️ Tech Stack

**Frontend:**
- Next.js 14 (App Router)
- React 18 + TypeScript
- Tailwind CSS
- Server-Sent Events (SSE)

**Backend:**
- FastAPI + Uvicorn
- LangGraph + LangChain
- OpenAI GPT-4o-mini
- Tavily Web Search API
- ArXiv API
- YouTube Search (no API key required)

**Deployment:**
- Frontend: Vercel
- Backend: Railway
- Database: In-memory (Redis ready)

## 📁 Project Structure

```
langgraph-ai-agent/
├── 🚀 Production Deployments
│   ├── backend/main.py          # Railway backend
│   └── frontend/               # Vercel frontend
├── 🤖 AI Agent Core
│   ├── src/agents/             # LangGraph workflows
│   ├── src/tools/              # AI tools (Tavily, ArXiv, YouTube)
│   └── src/utils/              # Configuration
├── 🎨 Frontend
│   ├── app/                    # Next.js app router
│   ├── components/             # React components
│   └── lib/                    # Services & utilities
├── 🧪 Development
│   ├── dev.py                  # Local dev server
│   └── tests/                  # Test suite
└── 📚 Documentation
    ├── README.md               # This file
    └── requirements.txt        # Dependencies
```

## � Quick Start

### Prerequisites
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))
- Tavily API Key ([Get one here](https://tavily.com)) - Optional for web search
- No additional API keys needed for YouTube search integration! 🎬

### Option 1: Use Live Demo
1. Visit the [live demo](https://myfirstadvanced-ipvmmodlp-inesaranabs-projects.vercel.app)
2. Click the ⚙️ settings icon
3. Enter your API keys
4. Try asking: "How do I learn React programming?" to see YouTube integration!
5. Start chatting!

### Option 2: Local Development

```bash
# 1. Clone repository
git clone https://github.com/inesaranab/langgraph-ai-agent.git
cd my_first_advanced_app

# 2. Backend setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Frontend setup
cd frontend
npm install

# 4. Run both services
# Terminal 1 (Backend):
python dev.py

# Terminal 2 (Frontend):
cd frontend
npm run dev
```

Visit: http://localhost:3000



## � Environment Variables

The app uses **user-provided API keys** for security. No server-side configuration needed!

For local development only:
```bash
# .env (optional - for default keys)
OPENAI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

## � API Reference

### Health Check
```bash
GET https://langgraph-ai-agent-production-561e.up.railway.app/health
```

### Chat (Streaming)
```bash
POST https://langgraph-ai-agent-production-561e.up.railway.app/chat/stream
Content-Type: application/json

{
  "message": "What's the latest in AI research?",
  "openai_api_key": "your-key",
  "tavily_api_key": "your-key",
  "session_id": "optional-session-id"
}
```



## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

## � License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- The **AI Makerspace** community ❤️
- **LangGraph** for the agent framework
- **OpenAI** for GPT models
- **Tavily** for web search capabilities
- **YouTube Search** library for educational video discovery
- **Vercel** & **Railway** for hosting

---

**Built with ❤️ by the LangGraph community**
