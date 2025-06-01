@echo off
chcp 65001 >nul
echo.
echo ===============================================
echo     โปรแกรมตัดและบีบอัดวิดีโอ (GUI)
echo ===============================================
echo.

cd /d "%~dp0"

if not exist "venv\" (
    echo สร้าง Virtual Environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ ไม่สามารถสร้าง Virtual Environment ได้
        pause
        exit /b 1
    )
)

echo เปิดใช้งาน Virtual Environment...
call venv\Scripts\activate.bat

if not exist "venv\Lib\site-packages\ffmpeg" (
    echo ติดตั้งไลบรารีที่จำเป็น...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ ไม่สามารถติดตั้งไลบรารีได้
        pause
        exit /b 1
    )
)

echo.
echo เริ่มโปรแกรม GUI...
echo.

python video_processor_gui.py

echo.
echo โปรแกรมปิดแล้ว
pause
