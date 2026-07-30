@echo off
echo SafeBite Platform - Development Server Launcher
echo =====================================================
echo.
echo Demo Accounts:
echo    Admin:    admin@safebite.demo / adminpassword
echo    Customer: customer@safebite.demo / password123
echo    Owner:    Any restaurant email / password123
echo.
echo Starting servers...
echo.

REM Check if database exists
if not exist "database\safebite.db" (
    echo Database not found! Please run setup first:
    echo    python setup.py
    pause
    exit /b 1
)

REM Start backend server
echo Starting FastAPI backend...
start "SafeBite Backend" cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment
timeout /t 3 /nobreak > nul

REM Start frontend server
echo Starting React frontend...
start "SafeBite Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Servers are starting...
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause > nul