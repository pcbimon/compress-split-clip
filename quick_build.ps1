# PowerShell Script สำหรับ Quick Build GUI + Portable
param()

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║              🚀 Quick Build GUI + Portable 🚀             ║" -ForegroundColor Cyan  
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ไปยัง directory ที่ถูกต้อง
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "🔧 เริ่มต้น build process..." -ForegroundColor Yellow
Write-Host ""

# รัน build script
& ".\build_portable.bat"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "🎉 Build เสร็จสิ้น!" -ForegroundColor Green
    Write-Host "📦 ไฟล์พร้อมใช้งาน:" -ForegroundColor Cyan
    
    if (Test-Path "dist\VideoProcessor_Portable.zip") {
        $zipSize = (Get-Item "dist\VideoProcessor_Portable.zip").Length / 1MB
        Write-Host "   - dist\VideoProcessor_Portable.zip ($("{0:N2}" -f $zipSize) MB)" -ForegroundColor White
    }
    
    if (Test-Path "dist\VideoProcessor_Portable") {
        Write-Host "   - dist\VideoProcessor_Portable\ (โฟลเดอร์พร้อมใช้)" -ForegroundColor White
    }
    
    Write-Host ""
    Write-Host "📂 เปิดดูผลลัพธ์..." -ForegroundColor Yellow
    Start-Process "explorer" -ArgumentList "dist"
    
    Write-Host ""
    Write-Host "✨ สำเร็จ! กด Enter เพื่อปิด..." -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ เกิดข้อผิดพลาดในการ build" -ForegroundColor Red
    Write-Host "กด Enter เพื่อปิด..." -ForegroundColor Yellow
}

Read-Host
