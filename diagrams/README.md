# LangGraph AI Agent - Workflow Diagrams

This directory contains the visual representation of the LangGraph AI Agent workflow.

## Files

### `complete_workflow.mmd`
Mermaid source file containing the complete workflow diagram with:
- **5-Node LangGraph Flow**: START → Analyzer → Tool Caller → Response Generator → Quality Checker → END
- **Multi-Tool Integration**: Web Search (Tavily) + Academic Search (ArXiv) + Educational Search (YouTube)
- **Smart Analysis Logic**: Query-based routing to appropriate tools
- **Quality Control**: Helpfulness scoring and response regeneration
- **State Management**: Complete AgentState field documentation

### `complete_workflow.png`
Generated PNG visualization of the complete workflow.

## Key Features Shown

✅ **YouTube Integration**: Educational content search with triggers like "tutorial", "how to", "guide"  
✅ **ArXiv Integration**: Academic paper search for research queries  
✅ **Web Search**: General information via Tavily API  
✅ **Quality Control**: GPT-based helpfulness evaluation with regeneration loop  
✅ **State Management**: Complete tracking of search results, tools used, and video content  

## Usage

To regenerate the PNG from the Mermaid source:
```bash
npx @mermaid-js/mermaid-cli -i complete_workflow.mmd -o complete_workflow.png
```

## Workflow Summary

1. **Query Analysis** → Determines which tools are needed based on content type
2. **Tool Execution** → Runs appropriate searches (Web/ArXiv/YouTube) 
3. **Response Generation** → Creates comprehensive answer with citations
4. **Quality Check** → Evaluates helpfulness and regenerates if needed
5. **Final Output** → Returns response with metadata and source tracking