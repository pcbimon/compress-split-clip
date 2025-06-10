#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
สคริปต์สำหรับสร้าง portable package ของ Video Processor
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_portable_package():
    """สร้าง portable package"""
    print("🔨 กำลังสร้าง Portable Package...")
      # กำหนดโฟลเดอร์
    base_dir = Path(__file__).parent
    dist_dir = base_dir / "dist"
    portable_dir = dist_dir / "VideoProcessor_Portable"
    
    # สร้างโฟลเดอร์ dist ถ้ายังไม่มี
    dist_dir.mkdir(exist_ok=True)
    
    # ลบโฟลเดอร์เก่าถ้ามี
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    
    # สร้างโฟลเดอร์ใหม่
    portable_dir.mkdir()
    
    # สร้างโครงสร้างโฟลเดอร์
    (portable_dir / "input_vdo").mkdir()
    (portable_dir / "output_vdo").mkdir()
    (portable_dir / "docs").mkdir()    # คัดลอกไฟล์ executable
    print("📦 คัดลอก executable files...")
    
    # ตรวจสอบว่ามีไฟล์ executable หรือไม่
    if not (dist_dir / "VideoProcessor.exe").exists() and not (dist_dir / "VideoProcessor_GUI.exe").exists():
        print("❌ ไม่พบไฟล์ executable ใน dist/")
        print("💡 กรุณารัน build script ก่อนเพื่อสร้าง executable files")
        return
    
    # คัดลอกและเปลี่ยนชื่อ GUI executable
    if (dist_dir / "VideoProcessor.exe").exists():
        shutil.copy2(dist_dir / "VideoProcessor.exe", portable_dir / "VideoProcessor_GUI.exe")
        print("✅ VideoProcessor_GUI.exe")
    elif (dist_dir / "VideoProcessor_GUI.exe").exists():
        shutil.copy2(dist_dir / "VideoProcessor_GUI.exe", portable_dir)
        print("✅ VideoProcessor_GUI.exe")
    
    if (dist_dir / "VideoProcessorCLI.exe").exists():
        shutil.copy2(dist_dir / "VideoProcessorCLI.exe", portable_dir)
        print("✅ VideoProcessorCLI.exe")
    
    # คัดลอกไฟล์ config
    if (base_dir / "config.json").exists():
        shutil.copy2(base_dir / "config.json", portable_dir)
        print("✅ config.json")
    
    # คัดลอกเอกสาร
    docs_files = [
        "README.md",
        "GUI_GUIDE.md", 
        "QUICKSTART.md"
    ]
    
    for doc_file in docs_files:
        if (base_dir / doc_file).exists():
            shutil.copy2(base_dir / doc_file, portable_dir / "docs")
            print(f"✅ {doc_file}")
    
    # สร้างไฟล์ launcher
    create_launcher_files(portable_dir)
    
    # สร้างไฟล์ README สำหรับ portable
    create_portable_readme(portable_dir)
    
    # สร้างไฟล์ zip
    create_zip_package(portable_dir)
    
    print(f"\n🎉 Portable Package สร้างเสร็จแล้ว!")
    print(f"📁 ตำแหน่ง: {portable_dir}")
    print(f"📦 ไฟล์ ZIP: {portable_dir}.zip")

def create_launcher_files(portable_dir):
    """สร้างไฟล์ launcher สำหรับ portable"""
    print("🚀 สร้าง launcher files...")
    
    # GUI Launcher
    gui_launcher = '''@echo off
chcp 65001 > nul
title Video Processor GUI
echo 🎬 Video Processor GUI
echo.
echo กำลังเปิด GUI...
start "" VideoProcessor_GUI.exe
'''
    
    with open(portable_dir / "Start_GUI.bat", "w", encoding="utf-8") as f:
        f.write(gui_launcher)
      # CLI Launcher
    cli_launcher = '''@echo off
chcp 65001 > nul
title Video Processor CLI

REM ===============================================
REM ตั้งค่าเริ่มต้น - แก้ไขค่าเหล่านี้ได้ตามต้องการ
REM ===============================================
SET Duration=60
SET LimitSize=25

REM Duration = ระยะเวลาการตัดแต่ละส่วน (วินาที)
REM LimitSize = ขนาดไฟล์สูงสุดแต่ละส่วน (MB)

echo ═══════════════════════════════════════════════
echo   🎬 Video Processor CLI - Quick Launch
echo ═══════════════════════════════════════════════
echo.
echo ค่าเริ่มต้นที่ตั้งไว้:
echo   📏 Duration: %Duration% วินาที
echo   💾 Limit Size: %LimitSize% MB
echo.
echo คำสั่งที่ใช้:
echo   VideoProcessorCLI.exe -d %Duration% -s %LimitSize%
echo.
echo ═══════════════════════════════════════════════
echo เลือกการทำงาน:
echo [1] ใช้ค่าเริ่มต้น (กด Enter)
echo [2] ใส่พารามิเตอร์เอง
echo [0] ออกจากโปรแกรม
echo ═══════════════════════════════════════════════
set /p choice="กรุณาเลือก (0-2) หรือกด Enter: "

if "%choice%"=="" set choice=1
if "%choice%"=="0" goto end
if "%choice%"=="1" goto quick_start
if "%choice%"=="2" goto custom_params

echo ❌ กรุณาเลือก 0, 1, 2 หรือกด Enter
pause
goto end

:quick_start
echo.
echo 🚀 เริ่มต้นด้วยค่าเริ่มต้น...
echo    Duration: %Duration% วินาที
echo    Limit Size: %LimitSize% MB
echo.
echo 💡 ใช้คำสั่ง: VideoProcessorCLI.exe -d %Duration% -s %LimitSize%
echo    หรือ: VideoProcessorCLI.exe --help เพื่อดูวิธีใช้งานทั้งหมด
echo.
VideoProcessorCLI.exe -d %Duration% -s %LimitSize%
goto end

:custom_params
echo.
echo 🛠️  โหมดกำหนดพารามิเตอร์เอง
echo ═══════════════════════════════════════════════
echo.
echo กรุณากำหนดค่าที่ต้องการ:
echo.

REM รับค่า Duration
set /p custom_duration="📏 ระยะเวลาการตัดแต่ละส่วน (วินาที) [ค่าเริ่มต้น: %Duration%]: "
if "%custom_duration%"=="" set custom_duration=%Duration%

REM รับค่า LimitSize  
set /p custom_limitsize="💾 ขนาดไฟล์สูงสุดแต่ละส่วน (MB) [ค่าเริ่มต้น: %LimitSize%]: "
if "%custom_limitsize%"=="" set custom_limitsize=%LimitSize%

echo.
echo ✅ ค่าที่เลือก:
echo    📏 Duration: %custom_duration% วินาที
echo    💾 Limit Size: %custom_limitsize% MB
echo.
echo 💡 คำสั่งที่จะใช้: VideoProcessorCLI.exe -d %custom_duration% -s %custom_limitsize%
echo.
set /p confirm="❓ ต้องการดำเนินการต่อหรือไม่? (Y/n): "
if /i "%confirm%"=="n" goto menu
if /i "%confirm%"=="no" goto menu

echo.
echo 🚀 เริ่มประมวลผลด้วยค่าที่กำหนด...
VideoProcessorCLI.exe -d %custom_duration% -s %custom_limitsize%
goto end

:end
echo.
pause
'''
    
    with open(portable_dir / "Start_CLI.bat", "w", encoding="utf-8") as f:
        f.write(cli_launcher)
    
    # Main Launcher Menu
    main_launcher = '''@echo off
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
'''
    
    with open(portable_dir / "Start.bat", "w", encoding="utf-8") as f:
        f.write(main_launcher)
    
    print("✅ Launcher files สร้างเสร็จแล้ว")

def create_portable_readme(portable_dir):
    """สร้างไฟล์ README สำหรับ portable package"""
    readme_content = '''# Video Processor - Portable Version

## 🎬 เกี่ยวกับโปรแกรม
Video Processor เป็นโปรแกรมสำหรับตัดและบีบอัดวิดีโอโดยใช้ FFmpeg
- ตัดวิดีโอเป็นส่วนๆ ตามเวลาที่กำหนด
- บีบอัดแต่ละส่วนให้มีขนาดไม่เกินที่กำหนด
- รองรับไฟล์วิดีโอทุกรูปแบบ
- มี GUI และ CLI mode

## 🚀 วิธีการใช้งาน

### เริ่มต้นใช้งาน
1. ดับเบิลคลิกที่ `Start.bat` เพื่อเปิดเมนูหลัก
2. เลือกโหมดที่ต้องการ:
   - **GUI Mode**: ใช้งานผ่านหน้าต่าง (แนะนำสำหรับผู้เริ่มต้น)
   - **CLI Mode**: ใช้งานผ่าน Command Line

### การใช้งาน GUI Mode
1. คลิก `Start_GUI.bat` หรือดับเบิลคลิกที่ `VideoProcessor_GUI.exe`
2. เลือกไฟล์วิดีโอที่ต้องการประมวลผล
3. กำหนดระยะเวลาการตัด (วินาที/นาที)
4. กำหนดขนาดไฟล์สูงสุด (MB)
5. คลิก "เริ่มประมวลผล"

### การใช้งาน CLI Mode
```bash
# ดูวิธีการใช้งาน
VideoProcessorCLI.exe --help

# ตัดวิดีโอเป็นส่วนๆ
VideoProcessorCLI.exe --input "video.mp4" --duration 60 --max-size 25
```

## 📁 โครงสร้างโฟลเดอร์
```
VideoProcessor_Portable/
├── Start.bat              # เมนูหลัก
├── Start_GUI.bat          # เปิด GUI Mode
├── Start_CLI.bat          # เปิด CLI Mode
├── VideoProcessor_GUI.exe # โปรแกรม GUI
├── VideoProcessorCLI.exe  # โปรแกรม CLI
├── config.json           # ไฟล์ตั้งค่า
├── input_vdo/            # วางไฟล์วิดีโอต้นฉบับ
├── output_vdo/           # ไฟล์ผลลัพธ์
└── docs/                 # เอกสารประกอบ
```

## ⚙️ ความต้องการของระบบ
- Windows 10/11
- FFmpeg (ดาวน์โหลดได้จาก https://ffmpeg.org/)
- เนื้อที่ว่างในฮาร์ดดิสก์เพียงพอ

## 📝 หมายเหตุ
- โปรแกรมนี้เป็น portable version ไม่ต้องติดตั้ง
- ต้องมี FFmpeg ในระบบเพื่อให้ทำงานได้
- สำหรับเอกสารฉบับเต็ม ดูในโฟลเดอร์ `docs/`

## 🆘 การแก้ไขปัญหา
หากเจอปัญหา:
1. ตรวจสอบว่าติดตั้ง FFmpeg แล้ว
2. ตรวจสอบสิทธิ์การเขียนไฟล์ในโฟลเดอร์
3. ดูเอกสารใน `docs/` สำหรับรายละเอียดเพิ่มเติม

---
© 2025 Video Processor - Portable Edition
'''
    
    with open(portable_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ README.txt สร้างเสร็จแล้ว")

def create_zip_package(portable_dir):
    """สร้างไฟล์ ZIP package"""
    print("📦 สร้างไฟล์ ZIP...")
    
    # สร้าง ZIP ไว้ในโฟลเดอร์ dist
    zip_path = portable_dir.parent / f"{portable_dir.name}.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(portable_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, portable_dir.parent)
                zipf.write(file_path, arc_name)
    
    # คำนวณขนาดไฟล์
    zip_size = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"✅ ZIP Package สร้างเสร็จแล้ว ({zip_size:.1f} MB)")

if __name__ == "__main__":
    try:
        create_portable_package()
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        import traceback
        traceback.print_exc()
