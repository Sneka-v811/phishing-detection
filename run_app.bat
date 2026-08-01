@echo off
echo ===================================================
echo   Starting AI Phishing Website Detector Web App...
echo ===================================================
cd /d C:\Users\Sneka\.gemini\antigravity\scratch\phishing-detection

:: Open browser automatically after 2 seconds
timeout /t 2 /nobreak >nul
start http://127.0.0.1:5000

:: Run Flask server
py app/app.py
pause
