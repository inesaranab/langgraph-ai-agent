#!/usr/bin/env python3
"""
Export Mermaid diagrams to PNG using mermaid-cli
Requires: npm install -g @mermaid-js/mermaid-cli
"""

import subprocess
import sys
import os
from pathlib import Path

def check_mermaid_cli():
    """Check if mermaid-cli is installed"""
    commands_to_try = ['mmdc', 'mmdc.cmd', 'mmdc.ps1']
    
    for cmd in commands_to_try:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True, check=True,
                                  shell=True)
            print(f"✅ Mermaid CLI found: {result.stdout.strip()}")
            return cmd
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    print("❌ Mermaid CLI not found. Please install with:")
    print("   npm install -g @mermaid-js/mermaid-cli")
    return None

def export_workflow_diagram():
    """Export the main workflow diagram to PNG"""
    mmdc_cmd = check_mermaid_cli()
    if not mmdc_cmd:
        return False
    
    workflow_file = Path("workflow.md")
    if not workflow_file.exists():
        print(f"❌ Workflow file not found: {workflow_file}")
        return False
    
    # Create output directory
    output_dir = Path("diagrams")
    output_dir.mkdir(exist_ok=True)
    
    try:
        # Export main workflow
        print("🎨 Exporting main workflow diagram...")
        subprocess.run([
            'mmdc', 
            '-i', str(workflow_file),
            '-o', str(output_dir / 'langgraph_workflow.png'),
            '--theme', 'default',
            '--width', '1200',
            '--height', '800'
        ], check=True)
        
        print(f"✅ Workflow diagram exported to: {output_dir}/langgraph_workflow.png")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Export failed: {e}")
        return False

def create_individual_diagrams():
    """Create individual Mermaid files for each diagram component"""
    
    # Main workflow
    main_workflow = '''
graph TD
    A[🚀 START] --> B[📊 Analyzer]
    
    B --> C{🤔 Should Use Tools?}
    C -->|needs_web_search OR needs_arxiv_search| D[🔧 Tool Caller]
    C -->|Simple query| E[🤖 Responder]
    
    D --> D1[🌐 Web Search<br/>Tavily API]
    D --> D2[📚 ArXiv Search<br/>Academic Papers]  
    D --> D3[🎥 YouTube Search<br/>Educational Videos]
    
    D1 --> E
    D2 --> E
    D3 --> E
    
    E --> F[⭐ Helpfulness Checker]
    
    F --> G{📈 Quality Check}
    G -->|Score < 0.3 AND iterations < 2| E
    G -->|Score >= 0.3 OR max iterations| H[✅ END]
    
    style A fill:#e1f5fe
    style H fill:#e8f5e8
    style C fill:#fff3e0
    style G fill:#fff3e0
    style D1 fill:#f3e5f5
    style D2 fill:#f3e5f5
    style D3 fill:#f3e5f5
'''

    # Architecture diagram
    architecture = '''
graph TB
    subgraph "🔧 Tool Layer"
        A[Tavily Search Tool]
        B[ArXiv Search Tool] 
        C[YouTube Search Tool]
        D[Helpfulness Checker]
    end
    
    subgraph "🧠 Agent Layer"
        E[LangGraph Agent]
        F[State Management]
    end
    
    subgraph "🌐 API Layer"
        G[FastAPI Backend]
        H[Streaming Endpoints]
    end
    
    subgraph "💻 Frontend Layer"
        I[React Chat UI]
        J[Source Citations]
    end
    
    A --> E
    B --> E
    C --> E
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J
'''

    diagrams = {
        'main_workflow.mmd': main_workflow,
        'architecture.mmd': architecture
    }
    
    output_dir = Path("diagrams")
    output_dir.mkdir(exist_ok=True)
    
    for filename, content in diagrams.items():
        file_path = output_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"📝 Created: {file_path}")
    
    return diagrams.keys()

def export_all_diagrams():
    """Export all individual diagram files to PNG"""
    if not check_mermaid_cli():
        return
    
    diagram_files = create_individual_diagrams()
    output_dir = Path("diagrams")
    
    for mmd_file in diagram_files:
        mmd_path = output_dir / mmd_file
        png_path = output_dir / mmd_file.replace('.mmd', '.png')
        
        try:
            print(f"🎨 Exporting {mmd_file}...")
            subprocess.run([
                'mmdc',
                '-i', str(mmd_path),
                '-o', str(png_path),
                '--theme', 'default',
                '--width', '1200',
                '--height', '800',
                '--backgroundColor', 'white'
            ], check=True)
            
            print(f"✅ Exported: {png_path}")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to export {mmd_file}: {e}")

def main():
    """Main execution function"""
    print("🚀 LangGraph Workflow Diagram Exporter")
    print("=" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--all':
        export_all_diagrams()
    else:
        export_workflow_diagram()
    
    print("\n📋 Usage:")
    print("  python export_diagrams.py        # Export main workflow only")
    print("  python export_diagrams.py --all  # Export all diagram components")

if __name__ == "__main__":
    main()