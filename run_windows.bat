@echo off
echo Starting SMA Backtester...
echo.
echo Make sure Docker Desktop is running!
echo.
docker start backtester_app || docker run -d -p 8501:8501 --name backtester_app SMA-backtester
echo.
echo App is running! Opening browser...
timeout /t 5
start http://localhost:8501