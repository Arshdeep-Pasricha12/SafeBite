#!/usr/bin/env python3
"""
SafeBite Setup Script
Automated setup for SafeBite Restaurant Platform
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(command, cwd=cwd, shell=shell, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {command}")
            return True
        else:
            print(f"❌ {command}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running {command}: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}.{version.micro}")
        return False

def check_node_version():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js {version} detected")
            return True
    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js 18+ from https://nodejs.org/")
        return False

def setup_backend():
    """Setup backend dependencies and database"""
    print("\n🔧 Setting up backend...")
    
    backend_dir = Path(__file__).parent / "backend"
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", cwd=backend_dir):
        print("⚠️  Try: python -m pip install -r requirements.txt")
        return False
    
    # Setup database
    print("\n📊 Setting up database...")
    database_dir = Path(__file__).parent / "database"
    
    if not run_command("python seed.py", cwd=database_dir):
        print("⚠️  Database setup failed. Check if all dependencies are installed.")
        return False
    
    # Check database
    db_path = database_dir / "safebite.db"
    if db_path.exists():
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM restaurants")
            restaurant_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            conn.close()
            
            print(f"✅ Database created with {restaurant_count} restaurants and {user_count} users")
            return True
        except Exception as e:
            print(f"❌ Database verification failed: {e}")
            return False
    else:
        print("❌ Database file not found")
        return False

def setup_frontend():
    """Setup frontend dependencies"""
    print("\n🎨 Setting up frontend...")
    
    frontend_dir = Path(__file__).parent / "frontend"
    
    # Install Node.js dependencies
    if not run_command("npm install", cwd=frontend_dir):
        print("⚠️  Frontend setup failed. Make sure Node.js is installed.")
        return False
    
    print("✅ Frontend dependencies installed")
    return True

def verify_setup():
    """Verify the setup is working"""
    print("\n🧪 Verifying setup...")
    
    # Check if all required files exist
    required_files = [
        "backend/app/main.py",
        "frontend/src/App.jsx",
        "database/safebite.db",
        "frontend/package.json",
        "backend/requirements.txt"
    ]
    
    base_path = Path(__file__).parent
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} not found")
            return False
    
    return True

def print_instructions():
    """Print instructions to start the application"""
    print("\n" + "="*60)
    print("🎉 SafeBite setup completed successfully!")
    print("="*60)
    print("\n📋 Demo Accounts:")
    print("   Admin:    admin@safebite.demo / adminpassword")
    print("   Customer: customer@safebite.demo / password123")
    print("   Owner:    Any restaurant email / password123")
    
    print("\n🚀 To start the application:")
    print("\n1. Start Backend (in terminal 1):")
    print("   cd backend")
    print("   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    
    print("\n2. Start Frontend (in terminal 2):")
    print("   cd frontend")
    print("   npm run dev")
    
    print("\n3. Access the application:")
    print("   Frontend: http://localhost:3000")
    print("   Backend API: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    
    print("\n📚 Documentation:")
    print("   README.md - Complete project overview")
    print("   docs/API_DOCUMENTATION.md - API reference")
    print("   docs/DEPLOYMENT_GUIDE.md - Production deployment")
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print("🏗️  SafeBite Setup Script")
    print("Setting up Restaurant Discovery & Safety Platform...")
    
    # Check prerequisites
    print("\n🔍 Checking prerequisites...")
    if not check_python_version():
        sys.exit(1)
    
    if not check_node_version():
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        print("\n❌ Backend setup failed")
        sys.exit(1)
    
    # Setup frontend  
    if not setup_frontend():
        print("\n❌ Frontend setup failed")
        sys.exit(1)
    
    # Verify setup
    if not verify_setup():
        print("\n❌ Setup verification failed")
        sys.exit(1)
    
    # Print instructions
    print_instructions()

if __name__ == "__main__":
    main()