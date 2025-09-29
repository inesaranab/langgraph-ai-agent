# LangGraph Workflow Diagrams

This folder contains visual representations of the actual LangGraph workflow extracted from the live agent code.

## Generated Diagrams

### 🏗️ `langgraph_workflow_actual.png`
**Main workflow extracted from the compiled LangGraph agent**

- Shows the actual 5-node workflow: Analyzer → Tool Caller → Responder → Helpfulness Checker
- Displays conditional routing based on `_should_use_tools()` and `_should_regenerate()`
- Represents the exact structure as built by `LangGraphAgent._build_graph()`

**Extracted Nodes**: `['__start__', 'analyzer', 'tool_caller', 'responder', 'helpfulness_checker']`

### 🔧 `tool_details.png`
**Detailed tool execution and analysis logic**

- Shows the internal logic of the Tool Caller node
- Details the analysis criteria for web search vs ArXiv search
- Explains the quality control evaluation process
- Maps the trigger words and conditions for each tool

### 📊 `state_flow.png`
**AgentState data flow through the workflow**

- Visualizes how the AgentState object evolves through each node
- Shows which fields are populated at each stage
- Tracks the data transformation from initial query to final response

## Source Files

- **`extract_workflow.py`**: Python script that rebuilds the actual LangGraph agent and extracts its structure
- **`*.mmd`**: Mermaid diagram source files
- **`*.png`**: Generated PNG images from Mermaid diagrams

## How It Works

1. The `extract_workflow.py` script imports the actual `LangGraphAgent` class
2. Builds the agent with dummy API keys to access the compiled graph structure
3. Extracts the real node names and connections from `agent.graph`
4. Generates accurate Mermaid diagrams reflecting the true workflow
5. Exports diagrams to PNG using `@mermaid-js/mermaid-cli`

## Accuracy

✅ **These diagrams represent the ACTUAL workflow structure**, not a theoretical or simplified version.

The script directly accesses:
- `compiled_graph.nodes`: Real node names from the LangGraph compilation
- `compiled_graph.channels`: State channels and routing information  
- Method signatures from the agent implementation

## Updates

To regenerate diagrams after code changes:
```bash
python extract_workflow.py
```

This ensures the visual documentation stays synchronized with the actual implementation.