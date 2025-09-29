# LangGraph AI Agent# LangGraph AI Agent# LangGraph AI Agent 🤖



> An intelligent multi-tool AI agent built with LangGraph that searches web, academic papers, and educational videos to provide comprehensive, cited responses.



## OverviewA sophisticated AI agent powered by LangGraph that provides comprehensive responses by intelligently searching across multiple knowledge sources including web search, academic papers, and educational videos.A production-ready AI agent application built with **LangGraph**, featuring a modern React frontend and FastAPI backend with full tool integration.



This application combines the power of LangGraph's workflow orchestration with multiple search tools to create an AI agent that can intelligently gather information from diverse sources and provide well-researched, cited responses.



**Live Application**: https://myfirstadvanced-r0yha9x6b-inesaranabs-projects.vercel.app## 🚀 Features## ✨ Features



## Key Features



- **Multi-Source Search**: Intelligently searches web (Tavily), academic papers (ArXiv), and educational videos (YouTube)- **🔍 Multi-Source Intelligence**: Combines web search, academic research, and educational content- **🧠 Advanced LangGraph Agent**: Intelligent workflow with conditional tool routing

- **Quality Assessment**: Built-in response evaluation system using GPT-based helpfulness scoring

- **Real-Time Streaming**: Fast, responsive chat interface with streaming responses- **💬 Real-Time Chat Interface**: Modern React-based UI with streaming responses  - **🌐 Web Search Integration**: Real-time information via Tavily API

- **Source Attribution**: Automatic citation and source tracking for all information

- **Smart Routing**: AI-driven tool selection based on query analysis- **📚 Source Citations**: Automatic tracking and citation of all information sources- **📚 Academic Search**: ArXiv paper search and analysis



## Architecture- **🎯 Smart Tool Selection**: AI-driven selection of optimal search tools per query- **📊 Quality Control**: Built-in helpfulness evaluation



**Frontend** (Next.js + TypeScript)- **⚡ High Performance**: FastAPI backend with optimized response streaming- **💬 Modern Chat UI**: React + Next.js with streaming responses

- Modern React-based chat interface

- Real-time streaming responses- **🎨 Modern Design**: Clean, responsive interface with dark theme- **🎨 Beautiful Design**: Black & gold themed interface

- Source panel with citations

- Responsive design with dark theme- **📱 Responsive**: Works on desktop and mobile



**Backend** (FastAPI + LangGraph)## 🛠 Tech Stack- **🔒 Secure**: User-provided API keys (no server-side key storage)

- LangGraph workflow orchestration

- Multi-tool agent with conditional routing

- Response quality evaluation

- RESTful API with streaming support### Backend## 🚀 Live Demo



**AI Tools**- **LangGraph** - Advanced AI agent workflow orchestration

- Web Search (Tavily API)

- Academic Search (ArXiv API) - **LangChain** - Tool integration and prompt engineering- **Frontend**: https://myfirstadvanced-ib93xxsdh-inesaranabs-projects.vercel.app

- Video Search (YouTube API)

- Helpfulness Evaluation (OpenAI GPT)- **FastAPI** - High-performance async API framework- **Backend API**: https://langgraph-ai-agent-production-561e.up.railway.app



## Quick Start- **OpenAI GPT-4** - Advanced language model- **API Docs**: https://langgraph-ai-agent-production-561e.up.railway.app/docs



### Prerequisites- **Tavily API** - Real-time web search

- Python 3.11+

- Node.js 18+- **ArXiv API** - Academic paper search## 🏗️ Architecture

- OpenAI API key

- Tavily API key- **YouTube Search** - Educational video discovery



### Setup```

```bash

# Clone repository### Frontend  ┌─────────────────┐    HTTPS/WSS    ┌──────────────────┐

git clone https://github.com/inesaranab/langgraph-ai-agent.git

cd langgraph-ai-agent- **Next.js 14** - Modern React framework with App Router│   Vercel        │ ──────────────► │   Railway        │



# Setup environment- **TypeScript** - Type-safe development│   Frontend      │                 │   Backend        │

cp .env.example .env

# Add your API keys to .env- **Tailwind CSS** - Utility-first styling│   - Next.js     │ ◄────────────── │   - FastAPI      │



# Install dependencies- **Streaming API** - Real-time response updates│   - React       │    JSON/SSE     │   - LangGraph    │

pip install -r requirements.txt

cd frontend && npm install && cd ..│   - TypeScript  │                 │   - AI Tools     │



# Launch application### Infrastructure└─────────────────┘                 └──────────────────┘

python dev.py

```- **Railway** - Backend cloud deployment```



## API Endpoints- **Vercel** - Frontend deployment and CDN



### Health Check- **Docker** - Containerized deployments## 🛠️ Tech Stack

```http

GET /health

```

## 🌐 Live Demo**Frontend:**

### Chat

```http- Next.js 14 (App Router)

POST /chat/stream

Content-Type: application/json**Production Application**: https://myfirstadvanced-r0yha9x6b-inesaranabs-projects.vercel.app- React 18 + TypeScript



{- Tailwind CSS

  "message": "Your question",

  "session_id": "unique-id",## ⚡ Quick Start- Server-Sent Events (SSE)

  "openai_api_key": "your-key",

  "tavily_api_key": "your-key"

}

```### Prerequisites**Backend:**



## Project Structure- Python 3.11+- FastAPI + Uvicorn



```- Node.js 18+- LangGraph + LangChain

├── backend/           # FastAPI server

├── frontend/          # Next.js application- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))- OpenAI GPT-4o-mini

├── src/

│   ├── agents/        # LangGraph agent implementation- Tavily API Key ([Get one here](https://tavily.com/))- Tavily Web Search API

│   ├── tools/         # Search and evaluation tools

│   └── utils/         # Configuration and utilities- ArXiv API

└── tests/            # Test suites

```### 1. Clone & Setup



## Deployment```bash**Deployment:**



- **Frontend**: Deployed on Vercelgit clone https://github.com/inesaranab/langgraph-ai-agent.git- Frontend: Vercel

- **Backend**: Deployed on Railway

- **Database**: Stateless (session-based)cd langgraph-ai-agent- Backend: Railway



## Tech Stack- Database: In-memory (Redis ready)



**Backend**: FastAPI, LangGraph, LangChain, OpenAI, Tavily, ArXiv  # Backend setup

**Frontend**: Next.js, TypeScript, Tailwind CSS  

**Infrastructure**: Railway, Vercel, Dockerpython -m venv .venv## 📁 Project Structure



## Contributingsource .venv/bin/activate  # Windows: .venv\Scripts\activate



1. Fork the repositorypip install -r requirements.txt```

2. Create a feature branch

3. Make your changeslanggraph-ai-agent/

4. Submit a pull request

# Frontend setup  ├── 🚀 Production Deployments

## License

cd frontend && npm install && cd ..│   ├── backend/main.py          # Railway backend

MIT License - see LICENSE file for details.
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
