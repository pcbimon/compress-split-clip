"""
โปรแกรมทดสอบการตัดและบีบอัดวิดีโอ (ไม่ต้องใช้ FFmpeg จริง)
ใช้สำหรับทดสอบว่าโค้ดทำงานถูกต้องหรือไม่
"""

import os
import time
import json
from pathlib import Path

class MockVideoProcessor:
    """Video Processor แบบจำลองสำหรับทดสอบ"""
    
    def __init__(self, input_folder="input_vdo", output_folder="output_vdo"):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.wmv', '*.flv', '*.webm', '*.m4v']
        
        # สร้างโฟลเดอร์ output
        Path(self.output_folder).mkdir(exist_ok=True)
        
        print("🧪 โหมดทดสอบ - ไม่ต้องใช้ FFmpeg")
    
    def get_video_files(self):
        """หาไฟล์วิดีโอทั้งหมด"""
        video_files = []
        input_path = Path(self.input_folder)
        
        for ext in ['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm', 'm4v']:
            video_files.extend(input_path.glob(f'*.{ext}'))
            video_files.extend(input_path.glob(f'*.{ext.upper()}'))
        
        return [str(f) for f in sorted(video_files)]
    
    def get_video_info(self, video_path):
        """จำลองข้อมูลวิดีโอ"""
        file_size = os.path.getsize(video_path)
        file_size_mb = file_size / (1024 * 1024)
        
        # จำลองข้อมูล (ใช้ขนาดไฟล์คำนวณความยาว)
        duration = file_size_mb * 60 / 100  # สมมติ 100 MB = 60 นาที
        bitrate = int(file_size * 8 / duration) if duration > 0 else 1000000
        
        return {
            'duration': duration,
            'bitrate': bitrate,
            'file_size_bytes': file_size,
            'file_size_mb': file_size_mb
        }
    
    def format_time(self, seconds):
        """แปลงวินาทีเป็นรูปแบบ HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def mock_split_and_compress(self, video_path, segment_duration, max_size_mb, quality_preset="medium"):
        """จำลองการตัดและบีบอัดวิดีโอ"""
        video_name = Path(video_path).stem
        video_info = self.get_video_info(video_path)
        total_duration = video_info['duration']
        
        if total_duration == 0:
            print(f"❌ ข้ามไฟล์ {video_path} - ไม่สามารถอ่านได้")
            return False
        
        import math
        num_segments = math.ceil(total_duration / segment_duration)
        
        print(f"\n📹 กำลังประมวลผล: {video_name} (โหมดทดสอบ)")
        print(f"⏱️  ความยาวรวม: {self.format_time(total_duration)} ({total_duration:.1f} วินาที)")
        print(f"📁 ขนาดต้นฉบับ: {video_info['file_size_mb']:.1f} MB")
        print(f"✂️  จะตัดเป็น {num_segments} ส่วน (ส่วนละ {segment_duration} วินาที)")
        print(f"🎯 เป้าหมายขนาดไฟล์: ไม่เกิน {max_size_mb} MB ต่อไฟล์")
        print("-" * 60)
        
        success_count = 0
        
        for i in range(min(num_segments, 3)):  # ทดสอบแค่ 3 ส่วนแรก
            start_time = i * segment_duration
            actual_duration = min(segment_duration, total_duration - start_time)
            
            output_filename = f"{video_name}_part{i+1:03d}.mp4"
            output_path = os.path.join(self.output_folder, output_filename)
            
            print(f"🔄 ส่วนที่ {i+1}/{num_segments}: {output_filename}")
            print(f"   ⏱️  เวลา: {self.format_time(start_time)} - {self.format_time(start_time + actual_duration)}")
            
            # จำลองการประมวลผล
            time.sleep(0.5)  # จำลองเวลาประมวลผล
            
            # สร้างไฟล์ทดสอบ
            with open(output_path, 'w') as f:
                f.write(f"Mock video file: {output_filename}\n")
                f.write(f"Original: {video_path}\n")
                f.write(f"Duration: {actual_duration} seconds\n")
                f.write(f"Target size: {max_size_mb} MB\n")
            
            # จำลองขนาดไฟล์
            mock_size_mb = max_size_mb * 0.8  # สมมติได้ขนาด 80% ของเป้าหมาย
            
            print(f"   ✅ สำเร็จ - ขนาด: {mock_size_mb:.1f} MB (จำลอง)")
            print(f"   ⚡ ใช้เวลา: 0.5 วินาที")
            print(f"   📉 อัตราบีบอัด: 5.0x (จำลอง)")
            print()
            
            success_count += 1
        
        if num_segments > 3:
            print(f"... (ข้าม {num_segments - 3} ส่วนที่เหลือในโหมดทดสอบ)")
        
        success_rate = (success_count / min(num_segments, 3)) * 100
        print(f"📊 สรุปการประมวลผล {video_name} (ทดสอบ):")
        print(f"   ✅ สำเร็จ: {success_count}/{min(num_segments, 3)} ส่วน ({success_rate:.1f}%)")
        
        return True
    
    def process_all_videos(self, segment_duration=300, max_size_mb=25, quality_preset="medium"):
        """จำลองการประมวลผลวิดีโอทั้งหมด"""
        video_files = self.get_video_files()
        
        if not video_files:
            print(f"❌ ไม่พบไฟล์วิดีโอในโฟลเดอร์ {self.input_folder}")
            return {'processed': 0, 'failed': 0, 'total': 0}
        
        print("🧪 โปรแกรมทดสอบตัดและบีบอัดวิดีโอ")
        print("=" * 60)
        print(f"📁 โฟลเดอร์ input: {self.input_folder}")
        print(f"📁 โฟลเดอร์ output: {self.output_folder}")
        print(f"📹 พบไฟล์วิดีโอ: {len(video_files)} ไฟล์")
        print(f"⚙️  ตั้งค่าทดสอบ:")
        print(f"   - ตัดทุก {segment_duration} วินาที ({self.format_time(segment_duration)})")
        print(f"   - ขนาดสูงสุด {max_size_mb} MB ต่อไฟล์")
        print(f"   - คุณภาพ: {quality_preset}")
        print("=" * 60)
        
        processed_count = 0
        failed_count = 0
        total_start_time = time.time()
        
        for idx, video_file in enumerate(video_files, 1):
            print(f"\n🎯 ไฟล์ที่ {idx}/{len(video_files)}: {os.path.basename(video_file)}")
            
            if self.mock_split_and_compress(video_file, segment_duration, max_size_mb, quality_preset):
                processed_count += 1
            else:
                failed_count += 1
        
        total_time = time.time() - total_start_time
        
        print("\n" + "=" * 60)
        print("🏁 สรุปการทดสอบ")
        print("=" * 60)
        print(f"✅ ประมวลผลสำเร็จ: {processed_count} ไฟล์")
        print(f"❌ ประมวลผลล้มเหลว: {failed_count} ไฟล์")
        print(f"📊 รวมทั้งหมด: {len(video_files)} ไฟล์")
        print(f"⏱️  เวลารวม: {self.format_time(total_time)}")
        print(f"📁 ไฟล์ทดสอบอยู่ในโฟลเดอร์: {self.output_folder}")
        print("\n💡 หมายเหตุ: นี่เป็นการทดสอบเท่านั้น ไม่ได้ประมวลผลวิดีโอจริง")
        print("💡 หากต้องการประมวลผลจริง ต้องติดตั้ง FFmpeg ก่อน")
        
        # บันทึกสรุปผล
        summary_file = os.path.join(self.output_folder, 'test_summary.json')
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump({
                'mode': 'test',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'settings': {
                    'segment_duration': segment_duration,
                    'max_size_mb': max_size_mb,
                    'quality_preset': quality_preset,
                    'input_folder': self.input_folder,
                    'output_folder': self.output_folder
                },
                'results': {
                    'processed': processed_count,
                    'failed': failed_count,
                    'total': len(video_files),
                    'time_taken': total_time
                }
            }, f, indent=2, ensure_ascii=False)
        
        print(f"📝 สรุปผลการทดสอบบันทึกในไฟล์: {summary_file}")
        
        return {
            'processed': processed_count,
            'failed': failed_count,
            'total': len(video_files),
            'time_taken': total_time
        }

def main():
    """รันการทดสอบ"""
    print("🧪 โหมดทดสอบ - โปรแกรมตัดและบีบอัดวิดีโอ")
    print("=" * 60)
    print("💡 โหมดนี้ไม่ต้องการ FFmpeg - เป็นการทดสอบการทำงานของโค้ดเท่านั้น")
    print("💡 หากต้องการประมวลผลจริง ให้ติดตั้ง FFmpeg แล้วใช้ video_processor.py")
    print("=" * 60)
    
    try:
        # สร้าง mock processor และรันทดสอบ
        processor = MockVideoProcessor()
        
        # ตั้งค่าทดสอบ
        segment_duration = 300  # 5 นาที
        max_size_mb = 25       # 25 MB
        quality_preset = "medium"
        
        # รันการทดสอบ
        result = processor.process_all_videos(segment_duration, max_size_mb, quality_preset)
        
        print(f"\n🎉 การทดสอบเสร็จสิ้น!")
        
    except KeyboardInterrupt:
        print("\n⏹️  การทดสอบถูกยกเลิก")
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาดในการทดสอบ: {e}")

if __name__ == "__main__":
    main()
    input("\nกดปุ่ม Enter เพื่อปิด...")
