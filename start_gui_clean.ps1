# PowerShell Script สำหรับรันโปรแกรม GUI ตัดและบีบอัดวิดีโอ (เวอร์ชันสะอาด)

param()

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "🎬 โปรแกรมตัดและบีบอัดวิดีโอ (GUI)" -ForegroundColor Cyan
Write-Host ("=" * 50) -ForegroundColor Cyan

# ไปยัง directory ที่ถูกต้อง
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# ตรวจสอบ Python
Write-Host "🔍 ตรวจสอบ Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ ไม่พบ Python" -ForegroundColor Red
    Write-Host "📥 กรุณาติดตั้ง Python จาก https://python.org" -ForegroundColor Yellow
    Read-Host "กดปุ่มใดๆ เพื่อปิด"
    exit 1
}

# ตรวจสอบ tkinter
Write-Host "🔍 ตรวจสอบ tkinter..." -ForegroundColor Yellow
try {
    $null = python -c "import tkinter" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ tkinter พร้อมใช้งาน" -ForegroundColor Green
    } else {
        throw "tkinter not found"
    }
} catch {
    Write-Host "❌ ไม่พบ tkinter" -ForegroundColor Red
    Write-Host "📥 กรุณาติดตั้ง Python แบบเต็ม (รวม tkinter)" -ForegroundColor Yellow
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

# ติดตั้ง dependencies
if (Test-Path "requirements.txt") {
    Write-Host "📦 ติดตั้งไลบรารี..." -ForegroundColor Yellow
    pip install -r requirements.txt --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ ไลบรารีพร้อมใช้งาน" -ForegroundColor Green
    } else {
        Write-Host "⚠️  มีปัญหาในการติดตั้งไลบรารี แต่จะดำเนินการต่อ" -ForegroundColor Yellow
    }
}

# สร้างโฟลเดอร์ output
if (-not (Test-Path "output_vdo")) {
    Write-Host "📁 สร้างโฟลเดอร์ output_vdo..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Name "output_vdo" | Out-Null
}

Write-Host ""
Write-Host "🚀 เริ่มโปรแกรม GUI..." -ForegroundColor Green
Write-Host "💡 หน้าต่างโปรแกรมจะเปิดขึ้นมา" -ForegroundColor Cyan
Write-Host ""

try {
    python video_processor_gui.py
    Write-Host ""
    Write-Host "✨ โปรแกรมปิดแล้ว" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "❌ เกิดข้อผิดพลาดในการรันโปรแกรม" -ForegroundColor Red
    Write-Host "รายละเอียด: $($_.Exception.Message)" -ForegroundColor Red
}

Read-Host "กดปุ่มใดๆ เพื่อปิดหน้าต่าง"
