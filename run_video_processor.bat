@echo off
chcp 65001 >nul
echo.
echo ===============================================
echo     โปรแกรมตัดและบีบอัดวิดีโอ
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

if not exist "venv\Scripts\ffmpeg-python*" (
    echo ติดตั้งไลบรารีที่จำเป็น...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ ไม่สามารถติดตั้งไลบรารีได้
        pause
        exit /b 1
    )
)

echo.
echo เริ่มโปรแกรม...
echo.

python video_processor.py --interactive

echo.
echo กดปุ่มใดๆ เพื่อปิดหน้าต่าง...
pause >nul
