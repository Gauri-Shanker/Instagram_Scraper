@echo off
echo [✔] Launching Instagram Multi-Bot Scraper...
cd /d "C:\Users\Lenovo\Desktop\paid\upwork"
call venv\Scripts\activate
python run_scraper_follower.py
echo.
echo [✔] All scraping tasks triggered. Press any key to close this window.
pause >nul
