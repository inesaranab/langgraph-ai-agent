@echo off
echo 🚀 LangGraph Workflow Diagram Exporter
echo ====================================

echo.
echo 📦 Installing Mermaid CLI (if not already installed)...
call npm install -g @mermaid-js/mermaid-cli

echo.
echo 🎨 Exporting diagrams...
python export_diagrams.py --all

echo.
echo ✅ Done! Check the 'diagrams' folder for PNG files.
pause