@echo off
echo Installing required packages...
pip install -r requirements.txt

echo.
echo Choose an option:
echo 1. Start Gemini Chat Application
echo 2. Check Available Models
echo 3. Check Models with Custom API Key
echo.
set /p option="Enter option (1, 2, or 3): "

if "%option%"=="1" (
    echo Starting Gemini Chat Application...
    python app.py
) else if "%option%"=="2" (
    echo Checking available models...
    python check_models.py
    pause
) else if "%option%"=="3" (
    echo.
    set /p api_key="Enter your Gemini API key: "
    echo Checking available models with your API key...
    python check_models.py %api_key%
    pause
) else (
    echo Invalid option. Starting Gemini Chat Application by default...
    python app.py
)