@echo off
chcp 65001 >nul
title Building Portable Video Processor

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║           🏗️  Building Portable Video Processor 🏗️        ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🔧 เปิดใช้งาน Virtual Environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ❌ ไม่พบ Virtual Environment
    echo กรุณารัน setup ก่อน
    pause
    exit /b 1
)

echo.
echo 📦 ตรวจสอบ PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo ติดตั้ง PyInstaller...
    pip install pyinstaller
)

echo.
echo 🗂️ สร้างโฟลเดอร์ dist...
if not exist "dist" mkdir dist
if not exist "build" mkdir build

echo.
echo 🎯 สร้าง GUI Executable...
echo กำลัง build... (อาจใช้เวลาสักครู่)
pyinstaller --clean video_processor_gui.spec

if errorlevel 0 (
    echo ✅ GUI Executable สร้างเสร็จแล้ว
) else (
    echo ❌ เกิดข้อผิดพลาดในการสร้าง GUI
)

echo.
echo 🖥️ สร้าง CLI Executable...
echo กำลัง build... (อาจใช้เวลาสักครู่)
pyinstaller --clean video_processor_cli.spec

if errorlevel 0 (
    echo ✅ CLI Executable สร้างเสร็จแล้ว
) else (
    echo ❌ เกิดข้อผิดพลาดในการสร้าง CLI
)

echo.
echo 📁 จัดระเบียบไฟล์...

if exist "dist\VideoProcessor.exe" (
    echo ✅ พบ VideoProcessor.exe (GUI)
    copy "dist\VideoProcessor.exe" "VideoProcessor_GUI.exe" >nul
)

if exist "dist\VideoProcessorCLI.exe" (
    echo ✅ พบ VideoProcessorCLI.exe (CLI)
    copy "dist\VideoProcessorCLI.exe" "VideoProcessor_CLI.exe" >nul
)

echo.
echo 📋 สร้างไฟล์แนะนำการใช้งาน...

echo # 🎬 Video Processor Portable > PORTABLE_README.txt
echo. >> PORTABLE_README.txt
echo ## วิธีใช้งาน >> PORTABLE_README.txt
echo. >> PORTABLE_README.txt
echo 1. **GUI Version**: ดับเบิลคลิก VideoProcessor_GUI.exe >> PORTABLE_README.txt
echo 2. **CLI Version**: ดับเบิลคลิก VideoProcessor_CLI.exe >> PORTABLE_README.txt
echo. >> PORTABLE_README.txt
echo ## ความต้องการ >> PORTABLE_README.txt
echo - ต้องมี FFmpeg ติดตั้งในระบบ >> PORTABLE_README.txt
echo - ดาวน์โหลดจาก: https://ffmpeg.org/download.html >> PORTABLE_README.txt
echo. >> PORTABLE_README.txt
echo ## หมายเหตุ >> PORTABLE_README.txt
echo - โปรแกรมนี้ไม่ต้องติดตั้ง Python >> PORTABLE_README.txt
echo - สามารถรันได้ทันทีบน Windows >> PORTABLE_README.txt
echo - ขนาดไฟล์อาจใหญ่เนื่องจากรวม Python runtime >> PORTABLE_README.txt

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                    🎉 Build เสร็จสิ้น! 🎉                ║
echo ╠═══════════════════════════════════════════════════════════╣
echo ║                                                           ║
echo ║  ไฟล์ที่สร้างแล้ว:                                       ║
echo ║  • VideoProcessor_GUI.exe - โปรแกรม GUI                 ║
echo ║  • VideoProcessor_CLI.exe - โปรแกรม Command Line        ║
echo ║  • PORTABLE_README.txt - คู่มือการใช้งาน                 ║
echo ║                                                           ║
echo ║  📂 ไฟล์อยู่ในโฟลเดอร์ปัจจุบัน                         ║
echo ║  📤 สามารถคัดลอกไปใช้งานเครื่องอื่นได้ทันที            ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

echo 📂 เปิดโฟลเดอร์ผลลัพธ์...
start .

echo.
echo ✨ การ build เสร็จสิ้น!
echo 💡 คัดลอกไฟล์ .exe ไปยังเครื่องอื่นเพื่อใช้งาน
echo.
pause
