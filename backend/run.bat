@echo off
REM Discord Clone Backend Runner for Windows

echo Starting Discord Clone Backend Server...
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Creating...
    python -m venv venv
    echo Virtual environment created.
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
if not exist "venv\requirements_installed.flag" (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo. > venv\requirements_installed.flag
    echo Dependencies installed.
    echo.
)

REM Check if .env exists
if not exist ".env" (
    echo Warning: .env file not found!
    echo Creating from .env.example...
    copy .env.example .env
    echo Please update .env with your configuration.
    echo.
)

REM Start server
echo Starting FastAPI server...
echo API: http://localhost:8000
echo Docs: http://localhost:8000/docs
echo ==========================================
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause