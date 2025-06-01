# 🎬 วิธีใช้งานโปรแกรมตัดและบีบอัดวิดีโอ

## ⚡ เริ่มต้นแบบเร็ว

### 1. วางไฟล์วิดีโอ
- วางไฟล์ `.mp4`, `.avi`, `.mov` หรือรูปแบบอื่นใน folder `input_vdo/`

### 2. รันโปรแกรม (เลือกวิธีใดวิธีหนึ่ง)

**วิธีที่ 1: ใช้ PowerShell (แนะนำ)**
```powershell
.\start.ps1
```

**วิธีที่ 2: ใช้ Batch File**
```cmd
run_video_processor.bat
```

**วิธีที่ 3: ใช้ Command Line**
```bash
python video_processor.py --interactive
```

### 3. ตั้งค่า
- **ระยะเวลาตัด**: กี่วินาทีต่อไฟล์ (เช่น 300 = 5 นาที)
- **ขนาดไฟล์**: ไม่เกินกี่ MB (เช่น 25 MB)
- **คุณภาพ**: fast/medium/slow

### 4. รอผลลัพธ์
- ไฟล์ที่ประมวลผลแล้วจะอยู่ใน folder `output_vdo/`

## 🎯 ตัวอย่างการใช้งาน

### สำหรับโซเชียล (Facebook, Instagram)
```bash
python video_processor.py -d 30 -s 10 -q fast
```
- ตัดทุก 30 วินาที
- ขนาดไม่เกิน 10 MB

### สำหรับ YouTube
```bash
python video_processor.py -d 300 -s 25 -q medium
```
- ตัดทุก 5 นาที
- ขนาดไม่เกิน 25 MB

### สำหรับเก็บถาวร
```bash
python video_processor.py -d 600 -s 100 -q slow
```
- ตัดทุก 10 นาที
- ขนาดไม่เกิน 100 MB

## 🔧 การแก้ไขปัญหา

**ปัญหา: ไม่พบ FFmpeg**
- ติดตั้ง FFmpeg จาก https://ffmpeg.org/download.html
- เพิ่ม FFmpeg ใน System PATH

**ปัญหา: ไฟล์ใหญ่เกินไป**
- ลดค่า `max_size_mb`
- เปลี่ยนเป็น `-q fast`

**ปัญหา: คุณภาพต่ำ**
- เพิ่มค่า `max_size_mb`
- เปลี่ยนเป็น `-q slow`

## 📁 โครงสร้างไฟล์

```
compress-split-clip/
├── input_vdo/              # วางวิดีโอที่นี่
├── output_vdo/             # ผลลัพธ์ที่นี่
├── video_processor.py      # โปรแกรมหลัก
├── start.ps1              # PowerShell launcher
├── run_video_processor.bat # Batch launcher
└── example.py             # ตัวอย่างการใช้งาน
```
