"""
Script to update all Railway and Vercel URLs to new deployments
Run this after creating fresh Railway and Vercel projects
"""
import os
import re
from pathlib import Path

# OLD URLs (current)
OLD_RAILWAY_URL = "https://langgraph-ai-agent-production-561e.up.railway.app"
OLD_VERCEL_URLS = [
    "https://myfirstadvanced-ipvmmodlp-inesaranabs-projects.vercel.app",
    "https://myfirstadvanced-jlxhx552d-inesaranabs-projects.vercel.app", 
    "https://myfirstadvanced-46vjx23bi-inesaranabs-projects.vercel.app",
    "https://myfirstadvanced-5zvy1jbt0-inesaranabs-projects.vercel.app"
]

# NEW URLs (replace these with your actual new URLs)
NEW_RAILWAY_URL = "https://langgraph-ai-agent-production-7799.up.railway.app"
NEW_VERCEL_URL = "YOUR_NEW_VERCEL_URL_HERE"    # e.g., "https://your-new-app.vercel.app"

def update_urls_in_project():
    """Update all URLs in the project"""
    
    if NEW_RAILWAY_URL == "YOUR_NEW_RAILWAY_URL_HERE" or NEW_VERCEL_URL == "YOUR_NEW_VERCEL_URL_HERE":
        print("❌ Please update the NEW_RAILWAY_URL and NEW_VERCEL_URL variables in this script first!")
        return
    
    project_root = Path(__file__).parent
    files_to_update = []
    
    # Files that contain Railway URLs
    railway_files = [
        "frontend/lib/chatService.ts",
        "frontend/vercel.json", 
        "frontend/next.config.js",
        "frontend/.env.production",
        "README.md",
        "test_fix_deployment.py",
        "debug_railway_api.py", 
        "test_chat_with_keys.py",
        "debug_404.py",
        "test_v2_deployment.py",
        "test_production_deployment.py"
    ]
    
    # Files that contain Vercel URLs  
    vercel_files = [
        "README.md",
        "test_v2_deployment.py",
        "test_production_deployment.py", 
        "debug_404.py"
    ]
    
    print("🔄 Updating Railway URLs...")
    for file_path in railway_files:
        full_path = project_root / file_path
        if full_path.exists():
            update_file_content(full_path, OLD_RAILWAY_URL, NEW_RAILWAY_URL)
            print(f"✅ Updated {file_path}")
        else:
            print(f"⚠️ File not found: {file_path}")
    
    print("\n🔄 Updating Vercel URLs...")
    for file_path in vercel_files:
        full_path = project_root / file_path
        if full_path.exists():
            content = full_path.read_text(encoding='utf-8')
            updated = False
            for old_url in OLD_VERCEL_URLS:
                if old_url in content:
                    content = content.replace(old_url, NEW_VERCEL_URL)
                    updated = True
            if updated:
                full_path.write_text(content, encoding='utf-8')
                print(f"✅ Updated {file_path}")
        else:
            print(f"⚠️ File not found: {file_path}")
    
    print("\n✅ All URLs updated successfully!")
    print(f"🚀 New Railway URL: {NEW_RAILWAY_URL}")
    print(f"🌐 New Vercel URL: {NEW_VERCEL_URL}")
    print("\n📝 Next steps:")
    print("1. Commit and push changes: git add . && git commit -m 'Update to fresh deployments' && git push")
    print("2. Test your new deployments!")

def update_file_content(file_path: Path, old_url: str, new_url: str):
    """Update a specific URL in a file"""
    try:
        content = file_path.read_text(encoding='utf-8')
        if old_url in content:
            updated_content = content.replace(old_url, new_url)
            file_path.write_text(updated_content, encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

if __name__ == "__main__":
    print("🔧 LangGraph AI Agent - Deployment URL Updater")
    print("=" * 50)
    update_urls_in_project()