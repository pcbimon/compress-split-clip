# Video Processor - Portable Version

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
