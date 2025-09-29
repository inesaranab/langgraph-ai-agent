# LangGraph AI Agent# LangGraph AI Agent 🤖



A sophisticated AI agent powered by LangGraph that provides comprehensive responses by intelligently searching across multiple knowledge sources including web search, academic papers, and educational videos.A production-ready AI agent application built with **LangGraph**, featuring a modern React frontend and FastAPI backend with full tool integration.



## 🚀 Features## ✨ Features



- **🔍 Multi-Source Intelligence**: Combines web search, academic research, and educational content- **🧠 Advanced LangGraph Agent**: Intelligent workflow with conditional tool routing

- **💬 Real-Time Chat Interface**: Modern React-based UI with streaming responses  - **🌐 Web Search Integration**: Real-time information via Tavily API

- **📚 Source Citations**: Automatic tracking and citation of all information sources- **📚 Academic Search**: ArXiv paper search and analysis

- **🎯 Smart Tool Selection**: AI-driven selection of optimal search tools per query- **📊 Quality Control**: Built-in helpfulness evaluation

- **⚡ High Performance**: FastAPI backend with optimized response streaming- **💬 Modern Chat UI**: React + Next.js with streaming responses

- **🎨 Modern Design**: Clean, responsive interface with dark theme- **🎨 Beautiful Design**: Black & gold themed interface

- **📱 Responsive**: Works on desktop and mobile

## 🛠 Tech Stack- **🔒 Secure**: User-provided API keys (no server-side key storage)



### Backend## 🚀 Live Demo

- **LangGraph** - Advanced AI agent workflow orchestration

- **LangChain** - Tool integration and prompt engineering- **Frontend**: https://myfirstadvanced-ib93xxsdh-inesaranabs-projects.vercel.app

- **FastAPI** - High-performance async API framework- **Backend API**: https://langgraph-ai-agent-production-561e.up.railway.app

- **OpenAI GPT-4** - Advanced language model- **API Docs**: https://langgraph-ai-agent-production-561e.up.railway.app/docs

- **Tavily API** - Real-time web search

- **ArXiv API** - Academic paper search## 🏗️ Architecture

- **YouTube Search** - Educational video discovery

```

### Frontend  ┌─────────────────┐    HTTPS/WSS    ┌──────────────────┐

- **Next.js 14** - Modern React framework with App Router│   Vercel        │ ──────────────► │   Railway        │

- **TypeScript** - Type-safe development│   Frontend      │                 │   Backend        │

- **Tailwind CSS** - Utility-first styling│   - Next.js     │ ◄────────────── │   - FastAPI      │

- **Streaming API** - Real-time response updates│   - React       │    JSON/SSE     │   - LangGraph    │

│   - TypeScript  │                 │   - AI Tools     │

### Infrastructure└─────────────────┘                 └──────────────────┘

- **Railway** - Backend cloud deployment```

- **Vercel** - Frontend deployment and CDN

- **Docker** - Containerized deployments## 🛠️ Tech Stack



## 🌐 Live Demo**Frontend:**

- Next.js 14 (App Router)

**Production Application**: https://myfirstadvanced-r0yha9x6b-inesaranabs-projects.vercel.app- React 18 + TypeScript

- Tailwind CSS

## ⚡ Quick Start- Server-Sent Events (SSE)



### Prerequisites**Backend:**

- Python 3.11+- FastAPI + Uvicorn

- Node.js 18+- LangGraph + LangChain

- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))- OpenAI GPT-4o-mini

- Tavily API Key ([Get one here](https://tavily.com/))- Tavily Web Search API

- ArXiv API

### 1. Clone & Setup

```bash**Deployment:**

git clone https://github.com/inesaranab/langgraph-ai-agent.git- Frontend: Vercel

cd langgraph-ai-agent- Backend: Railway

- Database: In-memory (Redis ready)

# Backend setup

python -m venv .venv## 📁 Project Structure

source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt```

langgraph-ai-agent/

# Frontend setup  ├── 🚀 Production Deployments

cd frontend && npm install && cd ..│   ├── backend/main.py          # Railway backend

```│   └── frontend/               # Vercel frontend

├── 🤖 AI Agent Core

### 2. Configure Environment│   ├── src/agents/             # LangGraph workflows

```bash│   ├── src/tools/              # AI tools (Tavily, ArXiv)

# Copy example environment file│   └── src/utils/              # Configuration

cp .env.example .env├── 🎨 Frontend

│   ├── app/                    # Next.js app router

# Edit .env with your API keys:│   ├── components/             # React components

# OPENAI_API_KEY=your_openai_key_here  │   └── lib/                    # Services & utilities

# TAVILY_API_KEY=your_tavily_key_here├── 🧪 Development

```│   ├── dev.py                  # Local dev server

│   └── tests/                  # Test suite

### 3. Launch Application└── 📚 Documentation

```bash    ├── README.md               # This file

# Start the full application (both backend and frontend)    └── requirements.txt        # Dependencies

python dev.py```

```

## � Quick Start

The application will be available at the URLs shown in the terminal output.

### Prerequisites

## 📡 API Reference- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))

- Tavily API Key ([Get one here](https://tavily.com)) - Optional for web search

### Health Check

```http### Option 1: Use Live Demo

GET /health1. Visit the [live demo](https://myfirstadvanced-ib93xxsdh-inesaranabs-projects.vercel.app)

```2. Click the ⚙️ settings icon

Returns system status and agent readiness.3. Enter your API keys

4. Start chatting!

### Chat (Complete Response)

```http### Option 2: Local Development

POST /chat

Content-Type: application/json```bash

# 1. Clone repository

{git clone https://github.com/inesaranab/langgraph-ai-agent.git

  "message": "Your question here",cd my_first_advanced_app

  "session_id": "unique-session-id", 

  "openai_api_key": "your-key",# 2. Backend setup

  "tavily_api_key": "your-key"python -m venv venv

}source venv/bin/activate  # Windows: venv\Scripts\activate

```pip install -r requirements.txt



### Chat (Streaming Response)# 3. Frontend setup

```httpcd frontend

POST /chat/streamnpm install

Content-Type: application/json

# 4. Run both services

{# Terminal 1 (Backend):

  "message": "Your question here",python dev.py

  "session_id": "unique-session-id",

  "openai_api_key": "your-key", # Terminal 2 (Frontend):

  "tavily_api_key": "your-key"cd frontend

}npm run dev

``````



## 🏗 Project ArchitectureVisit: http://localhost:3000



```

├── 🔧 backend/              # FastAPI REST API

├── 🎨 frontend/             # Next.js React application  ## � Environment Variables

├── 🤖 src/agents/           # LangGraph agent implementation

├── 🛠 src/tools/            # Search tool integrationsThe app uses **user-provided API keys** for security. No server-side configuration needed!

├── ⚙️ src/utils/            # Configuration management

├── 🧪 tests/               # Test suitesFor local development only:

├── 📦 Dockerfile           # Container configuration  ```bash

└── 📋 requirements.txt     # Python dependencies# .env (optional - for default keys)

```OPENAI_API_KEY=your_key_here

TAVILY_API_KEY=your_key_here

## 🔄 Agent Workflow```



1. **📥 Query Processing** - Analyzes user input and intent## � API Reference

2. **🎯 Tool Selection** - Intelligently selects optimal search tools  

3. **🔍 Information Gathering** - Executes parallel searches across sources### Health Check

4. **🧠 Response Synthesis** - Combines information into coherent responses```bash

5. **📖 Source Attribution** - Automatically cites all sources usedGET https://langgraph-ai-agent-production-561e.up.railway.app/health

```

## 🚀 Deployment

### Chat (Streaming)

### Railway Backend```bash

The backend is automatically deployed to Railway on every push to the main branch.POST https://langgraph-ai-agent-production-561e.up.railway.app/chat/stream

Content-Type: application/json

### Vercel Frontend  

The frontend is deployed to Vercel with automatic deployments configured.{

  "message": "What's the latest in AI research?",

### Docker  "openai_api_key": "your-key",

```bash  "tavily_api_key": "your-key",

# Build and run with Docker  "session_id": "optional-session-id"

docker build -t langgraph-agent .}

docker run -p 8000:8000 --env-file .env langgraph-agent```

```



## 🤝 Contributing

## 🤝 Contributing

1. Fork the repository

2. Create feature branch: `git checkout -b feature/amazing-feature`1. **Fork** the repository

3. Commit changes: `git commit -m 'Add amazing feature'`  2. **Create** a feature branch: `git checkout -b feature/amazing-feature`

4. Push to branch: `git push origin feature/amazing-feature`3. **Commit** changes: `git commit -m 'Add amazing feature'`

5. Submit a Pull Request4. **Push** to branch: `git push origin feature/amazing-feature`

5. **Open** a Pull Request

## 📄 License

## � License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

## 🙏 Acknowledgments

- [LangGraph](https://github.com/langchain-ai/langgraph) for agent orchestration

- [OpenAI](https://openai.com/) for language models- The **AI Makerspace** community ❤️

- [Tavily](https://tavily.com/) for web search capabilities- **LangGraph** for the agent framework

- [ArXiv](https://arxiv.org/) for academic paper access- **OpenAI** for GPT models

- **Tavily** for web search capabilities

---- **Vercel** & **Railway** for hosting



**Built with ❤️ using LangGraph, Next.js, and FastAPI**---

**Built with ❤️ by the LangGraph community**
