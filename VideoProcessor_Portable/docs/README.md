# 🎬 โปรแกรมตัดและบีบอัดวิดีโอ

โปรแกรม Python สำหรับการตัดและบีบอัดวิดีโอโดยใช้ FFmpeg พร้อมการควบคุมขนาดไฟล์

## 🎯 คุณสมบัติหลัก

- ✂️ **ตัดวิดีโอ**: แบ่งวิดีโอยาวเป็นช่วงๆ ตามเวลาที่กำหนด
- 📦 **บีบอัดขนาด**: ลดขนาดไฟล์ให้ไม่เกินที่กำหนด (MB)
- 🔍 **หาไฟล์อัตโนมัติ**: ค้นหาไฟล์วิดีโอทุกรูปแบบในโฟลเดอร์
- 📊 **แสดงความคืบหน้า**: ติดตามสถานะการประมวลผลแบบ real-time
- 🎚️ **ปรับคุณภาพได้**: เลือกระดับคุณภาพและความเร็วการเข้ารหัส
- 📝 **บันทึกสรุปผล**: สร้างรายงานการประมวลผลเป็นไฟล์ JSON

## 📋 ความต้องการระบบ

### 1. Python 3.7+
```bash
python --version
```

### 2. FFmpeg
- **Windows**: ดาวน์โหลดจาก [ffmpeg.org](https://ffmpeg.org/download.html)
- **การติดตั้ง**: แตกไฟล์และเพิ่ม `bin` folder ใน System PATH

### 3. Python Libraries
```bash
pip install -r requirements.txt
```

## 🚀 การติดตั้งและใช้งาน

### วิธีที่ 1: ใช้ Batch Script (แนะนำสำหรับ Windows)
```bash
# ดับเบิลคลิกที่ไฟล์
run_video_processor.bat
```

### วิธีที่ 2: ใช้ Command Line

#### ขั้นตอนที่ 1: สร้างและเปิดใช้งาน Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# หรือ source venv/bin/activate  # Linux/Mac
```

#### ขั้นตอนที่ 2: ติดตั้งไลบรารี
```bash
pip install -r requirements.txt
```

#### ขั้นตอนที่ 3: รันโปรแกรม
```bash
# โหมดโต้ตอบ (Interactive)
python video_processor.py --interactive

# โหมด Command Line
python video_processor.py -d 300 -s 25 -q medium
```

## 📁 โครงสร้างโฟลเดอร์

```
project/
├── input_vdo/          # วางไฟล์วิดีโอต้นฉบับที่นี่
│   ├── video1.mp4
│   ├── video2.avi
│   └── ...
├── output_vdo/         # ไฟล์ที่ประมวลผลแล้ว (สร้างอัตโนมัติ)
│   ├── video1_part001.mp4
│   ├── video1_part002.mp4
│   └── processing_summary.json
├── venv/              # Virtual Environment
├── video_processor.py # โปรแกรมหลัก
├── requirements.txt   # รายการไลบรารี
└── README.md         # ไฟล์นี้
```

## ⚙️ ตัวเลือกการใช้งาน

### Command Line Arguments
```bash
python video_processor.py [options]

Options:
  -d, --duration    ระยะเวลาการตัด (วินาที) [default: 300]
  -s, --size        ขนาดไฟล์สูงสุด (MB) [default: 25]
  -q, --quality     คุณภาพการเข้ารหัส [default: medium]
  -i, --input       โฟลเดอร์ input [default: input_vdo]
  -o, --output      โฟลเดอร์ output [default: output_vdo]
  --interactive     โหมดโต้ตอบ
```

### ระดับคุณภาพ (Quality Presets)
- `ultrafast` - เร็วที่สุด, ขนาดไฟล์ใหญ่
- `fast` - เร็ว
- `medium` - ปกติ (แนะนำ)
- `slow` - ช้า, คุณภาพดี
- `veryslow` - ช้าที่สุด, คุณภาพดีที่สุด

## 📄 รูปแบบวิดีโอที่รองรับ

- MP4 (`.mp4`)
- AVI (`.avi`)
- MOV (`.mov`)
- MKV (`.mkv`)
- WMV (`.wmv`)
- FLV (`.flv`)
- WebM (`.webm`)
- M4V (`.m4v`)

## 📊 ตัวอย่างการใช้งาน

### ตัวอย่างที่ 1: การใช้งานพื้นฐาน
```bash
# ตัดวิดีโอทุก 5 นาที (300 วินาที) ขนาดไฟล์ไม่เกิน 25 MB
python video_processor.py --interactive
```

### ตัวอย่างที่ 2: การใช้งานขั้นสูง
```bash
# ตัดทุก 10 นาที, ขนาดไม่เกิน 50 MB, คุณภาพสูง
python video_processor.py -d 600 -s 50 -q slow
```

### ตัวอย่างที่ 3: การกำหนดโฟลเดอร์เอง
```bash
python video_processor.py -i "my_videos" -o "processed_videos" -d 180 -s 15
```

## 📝 ไฟล์สรุปผล (processing_summary.json)

โปรแกรมจะสร้างไฟล์สรุปผลการประมวลผลใน `output_vdo/processing_summary.json`:

```json
{
  "timestamp": "2025-06-01 14:30:00",
  "settings": {
    "segment_duration": 300,
    "max_size_mb": 25,
    "quality_preset": "medium"
  },
  "results": {
    "processed": 2,
    "failed": 0,
    "total": 2,
    "time_taken": 145.6
  }
}
```

## 🔧 การแก้ไขปัญหา

### ปัญหา: ไม่พบ FFmpeg
```
❌ ข้อผิดพลาด: ไม่พบ FFmpeg หรือ FFprobe
```
**วิธีแก้**: ติดตั้ง FFmpeg และเพิ่มใน System PATH

### ปัญหา: ไฟล์ output ขนาดใหญ่เกินไป
- ลดค่า `max_size_mb`
- เปลี่ยน `quality_preset` เป็น `fast` หรือ `ultrafast`
- ลดค่า `segment_duration`

### ปัญหา: คุณภาพวิดีโอต่ำ
- เพิ่มค่า `max_size_mb`
- เปลี่ยน `quality_preset` เป็น `slow` หรือ `veryslow`

## 📞 การสนับสนุน

หากพบปัญหาหรือต้องการคำแนะนำ:
1. ตรวจสอบไฟล์ `processing_summary.json`
2. ตรวจสอบ System Requirements
3. ลองใช้ค่าเริ่มต้นก่อน

## 📄 License

โปรแกรมนี้เป็น Open Source สามารถใช้งานได้อย่างอิสระ

---
🎬 **Happy Video Processing!** 🎬
