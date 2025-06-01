@echo off
chcp 65001 > nul
title ตรวจสอบระบบ - Video Processor
color 0A

cls
echo ═══════════════════════════════════════════════
echo   🔍 ตรวจสอบความพร้อมของระบบ
echo ═══════════════════════════════════════════════
echo.

echo 🔧 ตรวจสอบ FFmpeg...
ffmpeg -version > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ FFmpeg พร้อมใช้งาน
    ffmpeg -version | findstr "ffmpeg version"
) else (
    echo ❌ ไม่พบ FFmpeg ในระบบ
    echo.
    echo 📥 วิธีการติดตั้ง FFmpeg:
    echo 1. ไปที่ https://ffmpeg.org/download.html
    echo 2. ดาวน์โหลดเวอร์ชัน Windows
    echo 3. แตกไฟล์และเพิ่ม path ใน System Environment
    echo 4. หรือวางไฟล์ ffmpeg.exe ในโฟลเดอร์เดียวกับโปรแกรม
    echo.
)

echo.
echo 📁 ตรวจสอบโฟลเดอร์...
if exist "input_vdo" (
    echo ✅ โฟลเดอร์ input_vdo พร้อมใช้งาน
) else (
    echo ⚠️  โฟลเดอร์ input_vdo ไม่พบ
    mkdir "input_vdo"
    echo ✅ สร้างโฟลเดอร์ input_vdo แล้ว
)

if exist "output_vdo" (
    echo ✅ โฟลเดอร์ output_vdo พร้อมใช้งาน
) else (
    echo ⚠️  โฟลเดอร์ output_vdo ไม่พบ
    mkdir "output_vdo"
    echo ✅ สร้างโฟลเดอร์ output_vdo แล้ว
)

echo.
echo 📊 ข้อมูลระบบ:
echo   OS: %OS%
echo   Processor: %PROCESSOR_ARCHITECTURE%
echo   User: %USERNAME%
echo   Computer: %COMPUTERNAME%

echo.
echo ═══════════════════════════════════════════════

ffmpeg -version > nul 2>&1
if %errorlevel% equ 0 (
    echo 🎉 ระบบพร้อมใช้งาน Video Processor!
    echo.
    echo 🚀 สามารถเริ่มใช้งานได้ด้วยคำสั่ง:
    echo   - GUI Mode: Start_GUI.bat
    echo   - CLI Mode: Start_CLI.bat
    echo   - เมนูหลัก: Start.bat
) else (
    echo ⚠️  กรุณาติดตั้ง FFmpeg ก่อนใช้งาน
)

echo.
pause
