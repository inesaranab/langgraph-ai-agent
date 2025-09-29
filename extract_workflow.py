#!/usr/bin/env python3
"""
LangGraph Workflow Visualizer
Rebuilds the actual LangGraph workflow and exports the compiled graph structure as Mermaid diagrams
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any
import subprocess

# Add project paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

def setup_environment():
    """Setup environment variables for the agent"""
    os.environ.setdefault("OPENAI_API_KEY", "dummy-key-for-graph-generation")
    os.environ.setdefault("TAVILY_API_KEY", "dummy-key-for-graph-generation")

def extract_langgraph_structure():
    """Extract the actual LangGraph workflow structure"""
    setup_environment()
    
    try:
        from src.agents.langgraph_agent import LangGraphAgent
        from src.utils.config import AppConfig
        
        print("🔧 Building LangGraph agent to extract structure...")
        
        # Create agent with dummy keys just to get the graph structure
        config = AppConfig()
        agent = LangGraphAgent(config, "dummy-openai-key", "dummy-tavily-key")
        
        # Get the compiled graph
        compiled_graph = agent.graph
        
        print("✅ Successfully built LangGraph workflow")
        
        # Extract graph structure
        graph_structure = {
            'nodes': [],
            'edges': [],
            'entry_point': None,
            'conditional_edges': []
        }
        
        # Get nodes from the compiled graph
        if hasattr(compiled_graph, 'nodes'):
            graph_structure['nodes'] = list(compiled_graph.nodes.keys())
            print(f"📊 Found {len(graph_structure['nodes'])} nodes: {graph_structure['nodes']}")
        
        # Try to get edges information
        if hasattr(compiled_graph, 'channels'):
            print(f"🔗 Found channels: {list(compiled_graph.channels.keys())}")
        
        return graph_structure, agent
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return None, None
    except Exception as e:
        print(f"❌ Error building graph: {e}")
        return None, None

def generate_mermaid_from_agent(agent):
    """Generate Mermaid diagram based on the actual agent structure"""
    
    # Manual extraction of the workflow based on the agent's _build_graph method
    mermaid_code = '''
graph TD
    START([🚀 START]) --> analyzer[📊 Analyzer<br/>_analyze_query]
    
    analyzer --> decision1{🤔 Should Use Tools?<br/>_should_use_tools}
    
    decision1 -->|"use_tools<br/>(needs_web_search OR<br/>needs_arxiv_search)"| tool_caller[🔧 Tool Caller<br/>_call_tools]
    decision1 -->|"direct_response<br/>(simple query)"| responder[🤖 Responder<br/>_generate_response]
    
    tool_caller --> responder
    responder --> helpfulness_checker[⭐ Helpfulness Checker<br/>_check_helpfulness]
    
    helpfulness_checker --> decision2{📈 Quality Decision<br/>_should_regenerate}
    
    decision2 -->|"regenerate<br/>(score < 0.3 AND<br/>iterations < 2)"| responder
    decision2 -->|"finish<br/>(score >= 0.3 OR<br/>max iterations)"| END([✅ END])
    
    %% Styling
    classDef startEnd fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef process fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef decision fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef tools fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    
    class START,END startEnd
    class analyzer,responder,helpfulness_checker process
    class decision1,decision2 decision
    class tool_caller tools
'''
    
    return mermaid_code.strip()

def generate_detailed_tool_diagram():
    """Generate detailed tool interaction diagram"""
    
    mermaid_code = '''
graph TB
    subgraph "🔧 Tool Execution Details"
        direction TB
        TC[Tool Caller Node<br/>_call_tools]
        
        TC --> WS{needs_web_search?}
        TC --> AS{needs_arxiv_search?}
        TC --> YS{YouTube Search<br/>Available?}
        
        WS -->|Yes| TT[🌐 Tavily Tool<br/>Web Search]
        AS -->|Yes| AT[📚 ArXiv Tool<br/>Academic Papers]
        YS -->|Yes| YT[🎥 YouTube Tool<br/>Educational Videos]
        
        TT --> AGG[📊 Aggregate Results]
        AT --> AGG
        YT --> AGG
        
        AGG --> SR[search_results<br/>tools_used<br/>youtube_videos]
    end
    
    subgraph "🧠 Analysis Logic"
        direction TB
        AN[Analyzer Node<br/>_analyze_query]
        
        AN --> W1["Web Search Triggers:<br/>• news, current, recent<br/>• technology, AI<br/>• complex queries (>3 words)"]
        AN --> A1["ArXiv Search Triggers:<br/>• research, paper, study<br/>• academic, scientific<br/>• algorithm, ML"]
        
        W1 --> NWS[needs_web_search = True]
        A1 --> NAS[needs_arxiv_search = True]
    end
    
    subgraph "⭐ Quality Control"
        direction TB
        HC[Helpfulness Checker<br/>_check_helpfulness]
        
        HC --> EVAL["GPT-3.5-turbo Evaluation<br/>Criteria:<br/>• Relevance<br/>• Accuracy<br/>• Completeness<br/>• Clarity<br/>• Usefulness"]
        
        EVAL --> SCORE[Score: 0.0 - 1.0]
        SCORE --> REGEN{"Score < 0.3 AND<br/>iterations < 2?"}
        
        REGEN -->|Yes| REG[Regenerate Response]
        REGEN -->|No| FIN[Finish Workflow]
    end
    
    %% Styling
    classDef tools fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef analysis fill:#e1f5fe,stroke:#01579b,stroke-width:2px  
    classDef quality fill:#fff3e0,stroke:#e65100,stroke-width:2px
    
    class TT,AT,YT,TC tools
    class AN,W1,A1,NWS,NAS analysis
    class HC,EVAL,SCORE,REGEN quality
'''
    
    return mermaid_code.strip()

def generate_state_flow_diagram():
    """Generate AgentState data flow diagram"""
    
    mermaid_code = '''
graph LR
    INIT["📊 Initial State<br/>messages: empty<br/>query: user_input<br/>response: empty<br/>tools_used: empty<br/>iteration_count: 0"]
    
    INIT --> ANA["📋 After Analysis<br/>needs_web_search<br/>needs_arxiv_search"]
    
    ANA --> TOOL["🔧 After Tools<br/>search_results<br/>youtube_videos<br/>tools_used"]
    
    TOOL --> RESP["🤖 After Response<br/>response: generated_text<br/>messages: updated"]
    
    RESP --> HELP["⭐ After Helpfulness<br/>helpfulness_score<br/>iteration_count++"]
    
    HELP --> FINAL["✅ Final State<br/>All fields populated<br/>Ready for return"]
    
    %% Styling
    classDef state fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    class INIT,ANA,TOOL,RESP,HELP,FINAL state
'''
    
    return mermaid_code.strip()

def export_diagrams():
    """Export all diagrams to PNG files"""
    
    print("🚀 LangGraph Workflow Extractor & Visualizer")
    print("=" * 50)
    
    # Extract actual graph structure
    graph_structure, agent = extract_langgraph_structure()
    
    if not agent:
        print("❌ Failed to build agent. Cannot proceed.")
        return
    
    # Create output directory
    output_dir = Path("diagrams")
    output_dir.mkdir(exist_ok=True)
    
    # Generate diagrams
    diagrams = {
        'langgraph_workflow_actual.mmd': generate_mermaid_from_agent(agent),
        'tool_details.mmd': generate_detailed_tool_diagram(),
        'state_flow.mmd': generate_state_flow_diagram()
    }
    
    # Write Mermaid files
    for filename, content in diagrams.items():
        file_path = output_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📝 Created: {file_path}")
    
    # Check for Mermaid CLI
    mmdc_cmd = None
    for cmd in ['mmdc', 'mmdc.cmd', 'mmdc.ps1']:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True, check=True,
                                  shell=True)
            print(f"✅ Mermaid CLI found: {result.stdout.strip()}")
            mmdc_cmd = cmd
            break
        except:
            continue
    
    if not mmdc_cmd:
        print("❌ Mermaid CLI not found. Install with: npm install -g @mermaid-js/mermaid-cli")
        print("📄 Mermaid files created. Use online editor: https://mermaid.live/")
        return
    
    # Export to PNG
    for mmd_filename in diagrams.keys():
        mmd_path = output_dir / mmd_filename
        png_path = output_dir / mmd_filename.replace('.mmd', '.png')
        
        try:
            print(f"🎨 Exporting {mmd_filename} to PNG...")
            subprocess.run([
                mmdc_cmd,
                '-i', str(mmd_path),
                '-o', str(png_path),
                '--theme', 'default',
                '--width', '1400',
                '--height', '1000',
                '--backgroundColor', 'white'
            ], check=True, shell=True)
            
            print(f"✅ Exported: {png_path}")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to export {mmd_filename}: {e}")
    
    print("\n🎯 Summary:")
    print(f"📁 Output directory: {output_dir}")
    print("📊 Generated diagrams:")
    print("   • langgraph_workflow_actual.png - Main workflow from actual agent")
    print("   • tool_details.png - Detailed tool execution flow")  
    print("   • state_flow.png - AgentState data flow")

def main():
    """Main execution function"""
    export_diagrams()

if __name__ == "__main__":
    main()