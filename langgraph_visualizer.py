"""
Generate PNG from actual compiled LangGraph using built-in visualization
"""

import sys
import os
import requests
import base64
import zlib
from io import BytesIO

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def create_agent_with_dummy_keys():
    """Create agent with dummy keys just for graph visualization"""
    try:
        from src.agents.langgraph_agent import LangGraphAgent
        from src.utils.config import AppConfig
        
        # Create dummy config
        class DummyConfig:
            def __init__(self):
                self.openai_api_key = "dummy-key-for-visualization"
                self.tavily_api_key = "dummy-key-for-visualization"
        
        config = DummyConfig()
        
        # Create agent with proper parameters
        agent = LangGraphAgent(
            config=config,
            openai_api_key="dummy-key-for-visualization",
            tavily_api_key="dummy-key-for-visualization"
        )
        
        print("✅ Created LangGraph agent successfully")
        return agent.graph
        
    except Exception as e:
        print(f"❌ Could not create agent: {e}")
        return None

def extract_mermaid_from_langgraph(compiled_graph):
    """Extract Mermaid code from compiled LangGraph and fix background"""
    try:
        print("📊 Attempting to extract graph structure...")
        
        # Method 1: Try get_graph() method
        if hasattr(compiled_graph, 'get_graph'):
            graph_info = compiled_graph.get_graph()
            print("✅ Found get_graph() method")
            
            # Try to get mermaid representation
            if hasattr(graph_info, 'draw_mermaid'):
                print("✅ Using draw_mermaid() method")
                raw_mermaid = graph_info.draw_mermaid()
                
                # Fix the transparent background issue
                fixed_mermaid = fix_background(raw_mermaid)
                return fixed_mermaid
                
            elif hasattr(graph_info, 'to_mermaid'):
                print("✅ Using to_mermaid() method")
                raw_mermaid = graph_info.to_mermaid()
                fixed_mermaid = fix_background(raw_mermaid)
                return fixed_mermaid
        
        # Method 2: Try direct mermaid methods on compiled graph
        if hasattr(compiled_graph, 'draw_mermaid'):
            print("✅ Using compiled_graph.draw_mermaid()")
            raw_mermaid = compiled_graph.draw_mermaid()
            fixed_mermaid = fix_background(raw_mermaid)
            return fixed_mermaid
        
        print("⚠️ Could not extract mermaid automatically")
        return None
        
    except Exception as e:
        print(f"⚠️ Could not extract mermaid: {e}")
        return None

def fix_background(raw_mermaid):
    """Fix the transparent background issue in the mermaid diagram"""
    print("🎨 Fixing transparent background...")
    
    # Simply replace the transparent fill with white background
    result = raw_mermaid.replace('classDef first fill-opacity:0', 'classDef first fill:#ffffff,stroke:#333333,stroke-width:2px')
    
    # Also ensure we have a white background for the whole diagram
    # Add background styling at the end
    if 'classDef default' in result:
        # Insert background styling after the existing classDef
        result = result.replace(
            'classDef default fill:#f2f0ff,line-height:1.2',
            'classDef default fill:#f2f0ff,line-height:1.2\n        classDef background fill:#ffffff'
        )
    
    return result

def generate_png_from_langgraph():
    """Generate PNG from actual compiled LangGraph"""
    
    print("🤖 Creating LangGraph agent...")
    compiled_graph = create_agent_with_dummy_keys()
    
    if compiled_graph is None:
        print("❌ Could not create graph")
        return None
    
    print("📊 Extracting Mermaid from compiled graph...")
    mermaid_content = extract_mermaid_from_langgraph(compiled_graph)
    
    if mermaid_content is None:
        print("❌ Could not extract mermaid")
        return None
    
    print("🎨 Generated Mermaid from actual LangGraph:")
    print("=" * 40)
    print(mermaid_content)
    print("=" * 40)
    
    # Generate PNG from the extracted mermaid
    return generate_png_from_mermaid_code(mermaid_content)

def generate_png_from_mermaid_code(mermaid_content):
    """Generate PNG using kroki.io service from mermaid code"""
    
    print("🌐 Generating PNG using kroki.io service...")
    
    try:
        # Compress the mermaid content
        compressed = zlib.compress(mermaid_content.encode('utf-8'))
        encoded = base64.urlsafe_b64encode(compressed).decode('utf-8')
        
        # Generate PNG using kroki.io
        url = f"https://kroki.io/mermaid/png/{encoded}"
        
        print(f"📡 Making request to kroki.io...")
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            # Save the PNG
            filename = "langgraph_workflow_diagram.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ PNG saved as '{filename}'")
            print(f"📊 File size: {len(response.content)} bytes")
            return filename
        else:
            print(f"❌ Failed to generate PNG: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error generating PNG: {e}")
        return None

def main():
    """Main function to generate the LangGraph visualization"""
    print("🚀 LangGraph Visualization Generator")
    print("=" * 50)
    
    # Try to generate from actual LangGraph first
    result = generate_png_from_langgraph()
    
    if result:
        print(f"\n🎉 Successfully generated: {result}")
        print("📋 You can now view the actual LangGraph workflow diagram!")
    else:
        print("\n❌ Failed to generate PNG")

if __name__ == "__main__":
    main()
