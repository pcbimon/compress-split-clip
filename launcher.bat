@echo off
chcp 65001 >nul
title Video Processor Launcher

:main
cls
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                🎬 Video Processor Suite 🎬               ║
echo ╠═══════════════════════════════════════════════════════════╣
echo ║                                                           ║
echo ║   1. 🖥️  GUI โปรแกรม (แนะนำ)                           ║
echo ║   2. 💻 Command Line โปรแกรม                             ║
echo ║   3. 🧪 ทดสอบระบบ                                      ║
echo ║   4. 📚 วิธีใช้งาน                                      ║
echo ║   5. 🚪 ออกจากโปรแกรม                                  ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

set /p choice="เลือกโปรแกรม (1-5): "

if "%choice%"=="1" goto gui
if "%choice%"=="2" goto cli
if "%choice%"=="3" goto test
if "%choice%"=="4" goto help
if "%choice%"=="5" goto exit
goto invalid

:gui
echo.
echo 🖥️  เริ่มโปรแกรม GUI...
echo.
call run_gui_clean.bat
goto main

:cli
echo.
echo 💻 เริ่มโปรแกรม Command Line...
echo.
call run_video_processor.bat
goto main

:test
echo.
echo 🧪 ทดสอบระบบ...
echo.
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    python system_check.py
) else (
    python system_check.py
)
pause
goto main

:help
echo.
echo 📚 เปิดคู่มือการใช้งาน...
echo.
if exist GUI_GUIDE.md (
    start notepad GUI_GUIDE.md
) else (
    echo ไม่พบไฟล์คู่มือ
)
if exist README.md (
    echo เปิด README.md...
    start notepad README.md
)
pause
goto main

:invalid
echo.
echo ❌ ตัวเลือกไม่ถูกต้อง กรุณาเลือก 1-5
pause
goto main

:exit
echo.
echo 👋 ขอบคุณที่ใช้บริการ!
echo.
timeout /t 2 >nul
exit /b 0
