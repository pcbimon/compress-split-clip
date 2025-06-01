@echo off
chcp 65001 >nul
title Quick Build - Video Processor

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║              🚀 Quick Build GUI + Portable 🚀             ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🔧 เริ่มต้น build process...
call build_portable.bat

echo.
echo 🎉 Build เสร็จสิ้น!
echo 📦 ไฟล์พร้อมใช้งาน:
echo    - dist\VideoProcessor_Portable.zip (สำหรับแจกจ่าย)
echo    - dist\VideoProcessor_Portable\ (โฟลเดอร์พร้อมใช้)
echo.

echo 📂 เปิดดูผลลัพธ์...
start "dist"

echo.
echo ✨ สำเร็จ! กด Enter เพื่อปิด...
pause >nul
