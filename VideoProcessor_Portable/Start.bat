@echo off
chcp 65001 > nul
title Video Processor - เมนูหลัก
color 0A

:menu
cls
echo ═══════════════════════════════════════════════
echo   🎬 Video Processor - Portable Version
echo ═══════════════════════════════════════════════
echo.
echo เลือกโหมดการทำงาน:
echo.
echo [1] GUI Mode - โหมดหน้าต่าง (แนะนำ)
echo [2] CLI Mode - โหมด Command Line
echo [3] เปิดโฟลเดอร์ Input
echo [4] เปิดโฟลเดอร์ Output
echo [5] ดูคู่มือการใช้งาน
echo [0] ออกจากโปรแกรม
echo.
echo ═══════════════════════════════════════════════
set /p choice="กรุณาเลือก (0-5): "

if "%choice%"=="1" (
    echo.
    echo 🚀 เปิด GUI Mode...
    start "" VideoProcessor_GUI.exe
    goto end
)
if "%choice%"=="2" (
    echo.
    echo 🚀 เปิด CLI Mode...
    VideoProcessorCLI.exe --help
    pause
    goto menu
)
if "%choice%"=="3" (
    echo.
    echo 📁 เปิดโฟลเดอร์ Input...
    start "" explorer "input_vdo"
    goto menu
)
if "%choice%"=="4" (
    echo.
    echo 📁 เปิดโฟลเดอร์ Output...
    start "" explorer "output_vdo"
    goto menu
)
if "%choice%"=="5" (
    echo.
    echo 📖 เปิดคู่มือการใช้งาน...
    start "" explorer "docs"
    goto menu
)
if "%choice%"=="0" (
    goto end
)

echo.
echo ❌ กรุณาเลือกหมายเลข 0-5 เท่านั้น
pause
goto menu

:end
echo.
echo 👋 ขอบคุณที่ใช้งาน Video Processor!
timeout /t 2 > nul
