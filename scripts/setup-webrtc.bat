@echo off
echo ========================================
echo Alpha WebRTC Setup
echo ========================================
echo.

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
    echo.
) else (
    echo Virtual environment already exists.
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.
echo Installing dependencies...
pip install "fastrtc[vad, tts]" numpy requests
echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo To run Alpha WebRTC, use:
echo   venv\Scripts\activate
echo   python alpha-webrtc.py
echo.
echo Or I can run it for you now. Run this file again!
echo.

REM Ask if user wants to run immediately
echo Press Y to run now, or any other key to exit...
set /p choice=
if /i "%choice%"=="Y" (
    echo Starting Alpha WebRTC...
    python alpha-webrtc.py
)