# PowerShell Script สำหรับรันโปรแกรมตัดและบีบอัดวิดีโอ
# Video Processor PowerShell Launcher

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "🎬 โปรแกรมตัดและบีบอัดวิดีโอ" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# ตรวจสอบว่าอยู่ใน directory ที่ถูกต้อง
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# ตรวจสอบ Python
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ไม่พบ Python" -ForegroundColor Red
    Write-Host "📥 กรุณาติดตั้ง Python จาก https://python.org" -ForegroundColor Yellow
    Read-Host "กดปุ่มใดๆ เพื่อปิด"
    exit 1
}

# ตรวจสอบ Virtual Environment
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "🔧 สร้าง Virtual Environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ ไม่สามารถสร้าง Virtual Environment ได้" -ForegroundColor Red
        Read-Host "กดปุ่มใดๆ เพื่อปิด"
        exit 1
    }
}

# เปิดใช้งาน Virtual Environment
Write-Host "🔄 เปิดใช้งาน Virtual Environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# ตรวจสอบและติดตั้ง dependencies
$requirementsPath = "requirements.txt"
if (Test-Path $requirementsPath) {
    Write-Host "📦 ตรวจสอบและติดตั้งไลบรารี..." -ForegroundColor Yellow
    pip install -r requirements.txt --quiet
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  มีปัญหาในการติดตั้งไลบรารี แต่จะดำเนินการต่อ" -ForegroundColor Yellow
    } else {
        Write-Host "✓ ไลบรารีพร้อมใช้งาน" -ForegroundColor Green
    }
}

# ตรวจสอบโฟลเดอร์ input
if (-not (Test-Path "input_vdo")) {
    Write-Host "📁 สร้างโฟลเดอร์ input_vdo..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Name "input_vdo" | Out-Null
}

$videoFiles = Get-ChildItem "input_vdo" -Include "*.mp4", "*.avi", "*.mov", "*.mkv", "*.wmv", "*.flv", "*.webm", "*.m4v" -File
Write-Host "📹 พบไฟล์วิดีโอ: $($videoFiles.Count) ไฟล์" -ForegroundColor Cyan

if ($videoFiles.Count -eq 0) {
    Write-Host "⚠️  ไม่พบไฟล์วิดีโอในโฟลเดอร์ input_vdo" -ForegroundColor Yellow
    Write-Host "📥 กรุณาวางไฟล์วิดีโอในโฟลเดอร์ input_vdo แล้วรันใหม่" -ForegroundColor Yellow
} else {
    Write-Host "📄 ไฟล์ที่พบ:" -ForegroundColor Cyan
    foreach ($file in $videoFiles) {
        $sizeGB = [math]::Round($file.Length / 1GB, 2)
        Write-Host "   - $($file.Name) ($sizeGB GB)" -ForegroundColor White
    }
}

Write-Host "`n🚀 เลือกโหมดการใช้งาน:" -ForegroundColor Cyan
Write-Host "1. โหมดโต้ตอบ (Interactive) - ถามค่าจากผู้ใช้" -ForegroundColor White
Write-Host "2. โหมดเร็ว - ตั้งค่าเริ่มต้น (ตัดทุก 5 นาที, 25 MB)" -ForegroundColor White
Write-Host "3. โหมด SNS - สำหรับโซเชียล (ตัดทุก 30 วินาที, 10 MB)" -ForegroundColor White
Write-Host "4. ดูตัวอย่างการใช้งาน" -ForegroundColor White
Write-Host "5. ออกจากโปรแกรม" -ForegroundColor White

$choice = Read-Host "`nเลือก (1-5)"

switch ($choice) {
    "1" {
        Write-Host "`n🎯 รันโหมดโต้ตอบ..." -ForegroundColor Green
        python video_processor.py --interactive
    }
    "2" {
        Write-Host "`n🎯 รันโหมดเร็ว..." -ForegroundColor Green
        python video_processor.py -d 300 -s 25 -q medium
    }
    "3" {
        Write-Host "`n🎯 รันโหมด SNS..." -ForegroundColor Green
        python video_processor.py -d 30 -s 10 -q fast
    }
    "4" {
        Write-Host "`n🎯 แสดงตัวอย่าง..." -ForegroundColor Green
        python example.py
    }
    "5" {
        Write-Host "`n👋 ขอบคุณที่ใช้บริการ!" -ForegroundColor Cyan
        exit 0
    }
    default {
        Write-Host "`n❌ ตัวเลือกไม่ถูกต้อง รันโหมดเริ่มต้น..." -ForegroundColor Yellow
        python video_processor.py --interactive
    }
}

Write-Host "`n✨ การประมวลผลเสร็จสิ้น!" -ForegroundColor Green
Read-Host "กดปุ่มใดๆ เพื่อปิดหน้าต่าง"
