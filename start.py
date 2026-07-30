#!/usr/bin/env python3
"""
SafeBite Start Script
Quick start script for development environment
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def run_backend():
    """Start the FastAPI backend server"""
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    print("🚀 Starting FastAPI backend on http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "app.main:app", 
        "--reload", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])

def run_frontend():
    """Start the React frontend server"""
    frontend_dir = Path(__file__).parent / "frontend"
    os.chdir(frontend_dir)
    
    print("🎨 Starting React frontend on http://localhost:3000")
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    subprocess.run(["npm", "run", "dev"])

def main():
    """Main function to start both servers"""
    print("🏗️  SafeBite Platform - Starting Development Servers")
    print("="*60)
    
    # Check if setup was run
    db_path = Path(__file__).parent / "database" / "safebite.db"
    if not db_path.exists():
        print("❌ Database not found! Please run setup first:")
        print("   python setup.py")
        sys.exit(1)
    
    print("📋 Demo Accounts:")
    print("   Admin:    admin@safebite.demo / adminpassword")
    print("   Customer: customer@safebite.demo / password123")
    print("   Owner:    Any restaurant email / password123")
    print("")
    
    try:
        # Start backend in a separate thread
        backend_thread = threading.Thread(target=run_backend)
        backend_thread.daemon = True
        backend_thread.start()
        
        # Start frontend in main thread
        run_frontend()
        
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down SafeBite servers...")
        sys.exit(0)

if __name__ == "__main__":
    main()