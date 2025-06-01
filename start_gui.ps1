# PowerShell Script สำหรับรันโปรแกรม GUI ตัดและบีบอัดวิดีโอ

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "🎬 โปรแกรมตัดและบีบอัดวิดีโอ (GUI)" -ForegroundColor Cyan
Write-Host ("=" * 50) -ForegroundColor Cyan

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

# ตรวจสอบ tkinter
try {
    python -c "import tkinter" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ tkinter พร้อมใช้งาน" -ForegroundColor Green
    } else {
        Write-Host "❌ ไม่พบ tkinter" -ForegroundColor Red
        Write-Host "📥 กรุณาติดตั้ง Python แบบเต็ม (รวม tkinter)" -ForegroundColor Yellow
        Read-Host "กดปุ่มใดๆ เพื่อปิด"
        exit 1
    }
} catch {
    Write-Host "⚠️  ไม่สามารถตรวจสอบ tkinter ได้" -ForegroundColor Yellow
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

# ตรวจสอบโฟลเดอร์ output
if (-not (Test-Path "output_vdo")) {
    Write-Host "📁 สร้างโฟลเดอร์ output_vdo..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Name "output_vdo" | Out-Null
}

Write-Host "`n🚀 เริ่มโปรแกรม GUI..." -ForegroundColor Green
Write-Host "💡 หน้าต่างโปรแกรมจะเปิดขึ้นมา" -ForegroundColor Cyan
Write-Host "💡 หากไม่เห็นหน้าต่าง ให้ตรวจสอบ taskbar" -ForegroundColor Cyan

try {
    python video_processor_gui.py
    Write-Host "`n✨ โปรแกรมปิดแล้ว" -ForegroundColor Green
} catch {
    Write-Host "`n❌ เกิดข้อผิดพลาดในการรันโปรแกรม" -ForegroundColor Red
    Write-Host "รายละเอียด: $($_.Exception.Message)" -ForegroundColor Red
}

Read-Host "`nกดปุ่มใดๆ เพื่อปิดหน้าต่าง"
