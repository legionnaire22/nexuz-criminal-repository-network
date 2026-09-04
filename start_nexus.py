"""
start_nexus.py
Launches the NEXUS FastAPI backend server.
Visit http://localhost:8000/docs for Swagger API Docs.
Open nexus/frontend/index.html in any browser for the Cytoscape dashboard.
"""

import os
import sys
import webbrowser

# Add backend directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print(" NEXUS v2.0 - Criminal Network Analysis System (SIH 2026)")
    print("="*60)
    print(" -> Backend API:  http://localhost:8000")
    print(" -> Swagger Docs: http://localhost:8000/docs")
    print(" -> Frontend Dev: Run 'npm run dev' in 'nexus/frontend' (http://localhost:5173)")
    print(" -> Static UI:    Open 'nexus/frontend/index.legacy.html' in browser")
    print("="*60 + "\n")
    
    uvicorn.run("main:app", app_dir=os.path.join(os.path.dirname(__file__), "backend"), host="127.0.0.1", port=8000, reload=True)
