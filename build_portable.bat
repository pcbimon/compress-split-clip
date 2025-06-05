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
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
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
echo 📁 จัดระเบียบไฟล์ในโฟลเดอร์ dist...

REM สร้างโฟลเดอร์ย่อยใน dist สำหรับ portable package
if not exist "dist\VideoProcessor_Portable" mkdir "dist\VideoProcessor_Portable"
if not exist "dist\VideoProcessor_Portable\input_vdo" mkdir "dist\VideoProcessor_Portable\input_vdo"
if not exist "dist\VideoProcessor_Portable\output_vdo" mkdir "dist\VideoProcessor_Portable\output_vdo"
if not exist "dist\VideoProcessor_Portable\docs" mkdir "dist\VideoProcessor_Portable\docs"

REM คัดลอก executable files ไปยัง dist
if exist "dist\VideoProcessor.exe" (
    echo ✅ พบ VideoProcessor.exe (GUI)
    copy "dist\VideoProcessor.exe" "dist\VideoProcessor_Portable\VideoProcessor_GUI.exe" >nul
    echo    → คัดลอกไปยัง dist\VideoProcessor_Portable\
)

if exist "dist\VideoProcessorCLI.exe" (
    echo ✅ พบ VideoProcessorCLI.exe (CLI)
    copy "dist\VideoProcessorCLI.exe" "dist\VideoProcessor_Portable\VideoProcessor_CLI.exe" >nul
    echo    → คัดลอกไปยัง dist\VideoProcessor_Portable\
)

REM คัดลอกไฟล์สำคัญไปยัง dist
if exist "config.json" (
    copy "config.json" "dist\VideoProcessor_Portable\" >nul
    echo ✅ คัดลอก config.json
)

if exist "README.md" (
    copy "README.md" "dist\VideoProcessor_Portable\docs\" >nul
    echo ✅ คัดลอก README.md
)

if exist "GUI_GUIDE.md" (
    copy "GUI_GUIDE.md" "dist\VideoProcessor_Portable\docs\" >nul
    echo ✅ คัดลอก GUI_GUIDE.md
)

if exist "QUICKSTART.md" (
    copy "QUICKSTART.md" "dist\VideoProcessor_Portable\docs\" >nul
    echo ✅ คัดลอก QUICKSTART.md
)

echo.
echo 📋 สร้างไฟล์แนะนำการใช้งานใน dist...

echo # 🎬 Video Processor Portable > "dist\VideoProcessor_Portable\README.txt"
echo. >> "dist\VideoProcessor_Portable\README.txt"
echo ## วิธีใช้งาน >> "dist\VideoProcessor_Portable\README.txt"
echo. >> "dist\VideoProcessor_Portable\README.txt"
echo 1. **GUI Version**: ดับเบิลคลิก VideoProcessor_GUI.exe >> "dist\VideoProcessor_Portable\README.txt"
echo 2. **CLI Version**: ดับเบิลคลิก VideoProcessor_CLI.exe >> "dist\VideoProcessor_Portable\README.txt"
echo. >> "dist\VideoProcessor_Portable\README.txt"
echo ## ความต้องการ >> "dist\VideoProcessor_Portable\README.txt"
echo - ต้องมี FFmpeg ติดตั้งในระบบ >> "dist\VideoProcessor_Portable\README.txt"
echo - ดาวน์โหลดจาก: https://ffmpeg.org/download.html >> "dist\VideoProcessor_Portable\README.txt"
echo. >> "dist\VideoProcessor_Portable\README.txt"
echo ## หมายเหตุ >> "dist\VideoProcessor_Portable\README.txt"
echo - โปรแกรมนี้ไม่ต้องติดตั้ง Python >> "dist\VideoProcessor_Portable\README.txt"
echo - สามารถรันได้ทันทีบน Windows >> "dist\VideoProcessor_Portable\README.txt"
echo - ขนาดไฟล์อาจใหญ่เนื่องจากรวม Python runtime >> "dist\VideoProcessor_Portable\README.txt"

REM สร้างไฟล์ batch สำหรับเรียกใช้งาน
echo @echo off > "dist\VideoProcessor_Portable\Start_GUI.bat"
echo chcp 65001 ^>nul >> "dist\VideoProcessor_Portable\Start_GUI.bat"
echo title Video Processor GUI >> "dist\VideoProcessor_Portable\Start_GUI.bat"
echo echo 🎬 Video Processor GUI >> "dist\VideoProcessor_Portable\Start_GUI.bat"
echo echo. >> "dist\VideoProcessor_Portable\Start_GUI.bat"
echo echo กำลังเปิด GUI... >> "dist\VideoProcessor_Portable\Start_GUI.bat"
echo start "" VideoProcessor_GUI.exe >> "dist\VideoProcessor_Portable\Start_GUI.bat"

echo @echo off > "dist\VideoProcessor_Portable\Start_CLI.bat"
echo chcp 65001 ^>nul >> "dist\VideoProcessor_Portable\Start_CLI.bat"
echo title Video Processor CLI >> "dist\VideoProcessor_Portable\Start_CLI.bat"
echo echo 🎬 Video Processor CLI >> "dist\VideoProcessor_Portable\Start_CLI.bat"
echo echo. >> "dist\VideoProcessor_Portable\Start_CLI.bat"
echo echo กำลังเปิด Command Line Interface... >> "dist\VideoProcessor_Portable\Start_CLI.bat"
echo echo ใช้ --help เพื่อดูวิธีการใช้งาน >> "dist\VideoProcessor_Portable\Start_CLI.bat"
echo echo. >> "dist\VideoProcessor_Portable\Start_CLI.bat"
echo VideoProcessor_CLI.exe %%* >> "dist\VideoProcessor_Portable\Start_CLI.bat"
echo pause >> "dist\VideoProcessor_Portable\Start_CLI.bat"

echo.
echo 📦 สร้างไฟล์ ZIP...
cd dist
powershell -Command "Compress-Archive -Path 'VideoProcessor_Portable' -DestinationPath 'VideoProcessor_Portable.zip' -Force"
if exist "VideoProcessor_Portable.zip" (
    echo ✅ สร้างไฟล์ ZIP สำเร็จ
    powershell -Command "(Get-Item 'VideoProcessor_Portable.zip').Length / 1MB | ForEach-Object { 'ขนาดไฟล์: {0:N2} MB' -f $_ }"
) else (
    echo ❌ ไม่สามารถสร้างไฟล์ ZIP ได้
)
cd ..

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                    🎉 Build เสร็จสิ้น! 🎉                ║
echo ╠═══════════════════════════════════════════════════════════╣
echo ║                                                           ║
echo ║  ไฟล์ที่สร้างแล้วใน dist\:                              ║
echo ║  • VideoProcessor_Portable.zip - ไฟล์ ZIP พร้อมใช้งาน    ║
echo ║  • VideoProcessor_Portable\ - โฟลเดอร์ portable         ║
echo ║    - VideoProcessor_GUI.exe - โปรแกรม GUI               ║
echo ║    - VideoProcessor_CLI.exe - โปรแกรม Command Line      ║
echo ║    - Start_GUI.bat - รัน GUI Mode                        ║
echo ║    - Start_CLI.bat - รัน CLI Mode                        ║
echo ║    - README.txt - คู่มือการใช้งาน                        ║
echo ║    - input_vdo\ - โฟลเดอร์สำหรับไฟล์วิดีโอต้นฉบับ      ║
echo ║    - output_vdo\ - โฟลเดอร์สำหรับไฟล์ผลลัพธ์           ║
echo ║                                                           ║
echo ║  📂 ไฟล์ทั้งหมดอยู่ในโฟลเดอร์ dist\                    ║
echo ║  📤 ส่งไฟล์ ZIP ให้ผู้อื่นใช้งานได้ทันที                ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

echo 📂 เปิดโฟลเดอร์ dist...
start "dist"

echo.
echo ✨ การ build เสร็จสิ้น!
echo 💡 ไฟล์ portable ทั้งหมดอยู่ในโฟลเดอร์ dist\
echo 📦 ไฟล์ ZIP พร้อมแจกจ่าย: dist\VideoProcessor_Portable.zip
echo 🎯 ขนาดกะทัดรัด พร้อมใช้งานทันทีบนเครื่องอื่น
echo.
pause
