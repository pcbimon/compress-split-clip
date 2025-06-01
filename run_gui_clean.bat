@echo off
chcp 65001 >nul
echo.
echo ===============================================
echo     โปรแกรมตัดและบีบอัดวิดีโอ (GUI)
echo ===============================================
echo.

cd /d "%~dp0"

echo ตรวจสอบ Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ไม่พบ Python
    echo 📥 กรุณาติดตั้ง Python จาก https://python.org
    pause
    exit /b 1
)

echo ตรวจสอบ tkinter...
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo ❌ ไม่พบ tkinter
    echo 📥 กรุณาติดตั้ง Python แบบเต็ม (รวม tkinter)
    pause
    exit /b 1
)

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

echo ติดตั้งไลบรารีที่จำเป็น...
pip install -r requirements.txt --quiet

if not exist "output_vdo\" (
    echo สร้างโฟลเดอร์ output_vdo...
    mkdir output_vdo
)

echo.
echo 🚀 เริ่มโปรแกรม GUI...
echo 💡 หน้าต่างโปรแกรมจะเปิดขึ้นมา
echo.

python video_processor_gui.py

echo.
echo ✨ โปรแกรมปิดแล้ว
pause
