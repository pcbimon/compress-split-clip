#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ตัวอย่างการใช้งานโปรแกรมตัดและบีบอัดวิดีโอ
"""

from video_processor import VideoProcessor
import time

def quick_demo():
    """ตัวอย่างการใช้งานแบบเร็ว"""
    print("🎬 ตัวอย่างการใช้งานโปรแกรมตัดและบีบอัดวิดีโอ")
    print("=" * 60)
    
    # สร้าง processor
    processor = VideoProcessor(
        input_folder="input_vdo",
        output_folder="output_vdo"
    )
    
    # ตรวจสอบไฟล์วิดีโอ
    video_files = processor.get_video_files()
    print(f"📹 พบไฟล์วิดีโอ: {len(video_files)} ไฟล์")
    
    if not video_files:
        print("❌ ไม่พบไฟล์วิดีโอ กรุณาใส่ไฟล์ใน folder input_vdo")
        return
    
    # แสดงข้อมูลไฟล์แรก
    first_video = video_files[0]
    video_info = processor.get_video_info(first_video)
    
    print(f"\n📄 ข้อมูลไฟล์ตัวอย่าง: {first_video}")
    print(f"   ⏱️  ความยาว: {processor.format_time(video_info['duration'])}")
    print(f"   📁 ขนาด: {video_info['file_size_mb']:.1f} MB")
    print(f"   📊 Bitrate: {video_info['bitrate']//1000}k")

def custom_processing():
    """ตัวอย่างการกำหนดค่าเอง"""
    print("\n🛠️  ตัวอย่างการประมวลผลแบบกำหนดเอง")
    print("-" * 60)
    
    # การตั้งค่าต่างๆ
    settings = [
        {"name": "ไฟล์เล็ก (SNS)", "duration": 30, "size": 5, "quality": "fast"},
        {"name": "ไฟล์กลาง (YouTube)", "duration": 300, "size": 25, "quality": "medium"},
        {"name": "ไฟล์ใหญ่ (Archive)", "duration": 600, "size": 100, "quality": "slow"}
    ]
    
    for i, setting in enumerate(settings, 1):
        print(f"{i}. {setting['name']}")
        print(f"   - ตัดทุก {setting['duration']} วินาที")
        print(f"   - ขนาดสูงสุด {setting['size']} MB")
        print(f"   - คุณภาพ: {setting['quality']}")

def batch_processing_example():
    """ตัวอย่างการประมวลผลแบบ batch"""
    print("\n🔄 ตัวอย่างการประมวลผลหลายไฟล์")
    print("-" * 60)
    
    processor = VideoProcessor()
    
    # ตัวอย่างการรันแบบ batch
    result = processor.process_all_videos(
        segment_duration=180,  # 3 นาที
        max_size_mb=15,        # 15 MB
        quality_preset="medium"
    )
    
    print(f"📊 ผลลัพธ์:")
    print(f"   ✅ สำเร็จ: {result['processed']} ไฟล์")
    print(f"   ❌ ล้มเหลว: {result['failed']} ไฟล์")
    print(f"   ⏱️  เวลารวม: {result['time_taken']:.1f} วินาที")

if __name__ == "__main__":
    try:
        # รันตัวอย่าง
        quick_demo()
        custom_processing()
        
        # ถามผู้ใช้ว่าต้องการรันจริงหรือไม่
        print("\n" + "=" * 60)
        choice = input("🤔 ต้องการทดสอบการประมวลผลจริงหรือไม่? (y/N): ").lower()
        
        if choice in ['y', 'yes', 'ใช่']:
            batch_processing_example()
        else:
            print("💡 หากต้องการรันจริง ใช้คำสั่ง:")
            print("   python video_processor.py --interactive")
            
    except KeyboardInterrupt:
        print("\n⏹️  โปรแกรมถูกยกเลิก")
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")
