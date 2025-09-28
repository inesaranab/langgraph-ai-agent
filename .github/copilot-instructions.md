<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->
- [x] Verify that the copilot-instructions.md file in the .github directory is created.

- [x] Clarify Project Requirements
	Project: LangGraph AI Agent Web Application with React frontend and FastAPI backend
	Language: Python (backend), TypeScript/JavaScript (frontend)
	Frameworks: LangGraph, LangChain, FastAPI, React, Next.js
	Features: Agent workflow, tool integration, state management, modern web interface

- [x] Scaffold the Project
	Created complete LangGraph AI Agent application structure:
	- src/: Main application code with agents, tools, and utilities
	- tests/: Unit tests for components
	- config/: Configuration files
	- Docker deployment support
	- Launch scripts and documentation

- [x] Customize the Project
	Customized application based on LangGraph notebook inspiration:
	- React + Next.js frontend with modern UI
	- FastAPI backend with REST API
	- LangGraph workflow with conditional tool usage
	- Tavily web search and ArXiv academic search integration
	- Helpfulness evaluation and quality control
	- Session management and conversation history
	- Vercel deployment configuration

- [x] Install Required Extensions
	No specific VS Code extensions required for this React/FastAPI project.

- [x] Compile the Project
	Successfully installed all dependencies:
	- Backend: FastAPI, LangGraph, LangChain, OpenAI, Tavily, ArXiv
	- Frontend: React, Next.js, TypeScript, Tailwind CSS
	- Development tools: pytest, black, flake8
	- Utilities: python-dotenv, pydantic

- [x] Create and Run Task
	Created and tested VS Code task to run the LangGraph AI Agent application.
	Task successfully detects missing .env file and validates dependencies.

- [ ] Launch the Project
	Ready to launch! User needs to:
	1. Copy .env.example to .env
	2. Add OpenAI and Tavily API keys
	3. Run: python dev.py (or use VS Code task)

- [ ] Ensure Documentation is Complete
	README.md ✅ Complete with installation and usage instructions
	.env.example ✅ Configured with all required environment variables
	Dockerfile ✅ Ready for containerized deployment
	Launch script ✅ Automated startup with dependency checks