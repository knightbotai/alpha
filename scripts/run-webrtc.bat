@echo off
REM Alpha WebRTC - Auto-Setup and Run
REM Just double-click this file!

echo ========================================
echo Alpha WebRTC - Setting up...
echo ========================================
echo.

REM Get directory of this script
set SCRIPT_DIR=%~dp0
cd /d %SCRIPT_DIR%

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo [1/3] Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo [2/3] Activating environment...
call venv\Scripts\activate.bat

REM Install dependencies if needed
pip install "fastrtc[vad, tts]" numpy requests >nul 2>&1
echo [3/3] Dependencies ready!
echo.

echo ========================================
echo Starting Alpha WebRTC...
echo ========================================
echo.
echo If a browser doesn't open, go to:
echo http://localhost:7860
echo.
echo Press Ctrl+C to stop.
echo.

REM Run the script
python alpha-webrtc.py

pause