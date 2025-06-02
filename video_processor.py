import os
import glob
import math
import time
import json
import argparse
import subprocess
import ffmpeg
from pathlib import Path
from typing import List, Tuple

class VideoProcessor:
    def __init__(self, input_folder: str = "input_vdo", output_folder: str = "output_vdo"):
        """
        สร้าง VideoProcessor สำหรับการตัดและบีบอัดวิดีโอ
        
        Args:
            input_folder: โฟลเดอร์ที่เก็บไฟล์วิดีโอต้นฉบับ
            output_folder: โฟลเดอร์สำหรับเก็บไฟล์ที่ประมวลผลแล้ว
        """
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.wmv', '*.flv', '*.webm', '*.m4v']
        
        # สร้างโฟลเดอร์ output หากไม่มี
        Path(self.output_folder).mkdir(exist_ok=True)
        
        # ตรวจสอบว่ามี ffmpeg หรือไม่
        self._check_ffmpeg()
    
    def _check_ffmpeg(self):
        """ตรวจสอบว่ามี FFmpeg ติดตั้งในระบบหรือไม่"""
        try:
            # ใช้ ffmpeg-python ในการตรวจสอบ
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            print("✓ FFmpeg พร้อมใช้งาน")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ ข้อผิดพลาด: ไม่พบ FFmpeg หรือ FFprobe")
            print("📥 กรุณาติดตั้ง FFmpeg ก่อนใช้งาน")
            print("🔗 ดาวน์โหลดได้จาก: https://ffmpeg.org/download.html")
            raise SystemExit("FFmpeg ไม่พร้อมใช้งาน")
    
    def get_video_files(self) -> List[str]:
        """หาไฟล์วิดีโอทั้งหมดในโฟลเดอร์ input"""
        video_files = []
        for extension in self.video_extensions:
            pattern = os.path.join(self.input_folder, extension)
            video_files.extend(glob.glob(pattern))
        return sorted(video_files)
    
    def get_video_info(self, video_path: str) -> dict:
        """หาข้อมูลของวิดีโอ (ความยาว, bitrate, ขนาดไฟล์)"""
        try:
            # ใช้ ffmpeg-python ในการหาข้อมูลวิดีโอ
            probe = ffmpeg.probe(video_path)
            
            # หาข้อมูล format
            format_info = probe['format']
            duration = float(format_info.get('duration', 0))
            bitrate = int(format_info.get('bit_rate', 0))
            
            # หาขนาดไฟล์
            file_size = os.path.getsize(video_path)
            file_size_mb = file_size / (1024 * 1024)
            
            return {
                'duration': duration,
                'bitrate': bitrate,
                'file_size_bytes': file_size,
                'file_size_mb': file_size_mb
            }
        except Exception as e:
            print(f"❌ ไม่สามารถอ่านข้อมูลไฟล์ {video_path}: {e}")
            return {'duration': 0, 'bitrate': 0, 'file_size_bytes': 0, 'file_size_mb': 0}
    
    def calculate_target_bitrate(self, duration_seconds: float, max_size_mb: float) -> int:
        """คำนวณ bitrate ที่ต้องการให้ได้ขนาดไฟล์ตามที่กำหนด"""
        if duration_seconds <= 0:
            return 1000000  # default 1Mbps
        
        # แปลง MB เป็น bits และคำนวณ bitrate
        max_size_bits = max_size_mb * 8 * 1024 * 1024
        target_bitrate = int(max_size_bits / duration_seconds)
        
        # ลด 25% เพื่อความปลอดภัย (สำหรับ audio และ overhead)
        return max(int(target_bitrate * 0.75), 100000)  # อย่างต่ำ 100kbps
    
    def format_time(self, seconds: float) -> str:
        """แปลงวินาทีเป็นรูปแบบ HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def split_and_compress_video(self, video_path: str, segment_duration: int, max_size_mb: float, 
                               quality_preset: str = "medium") -> bool:
        """
        ตัดและบีบอัดวิดีโอด้วย ffmpeg-python
        
        Args:
            video_path: เส้นทางไฟล์วิดีโอ
            segment_duration: ระยะเวลาการตัดในวินาที
            max_size_mb: ขนาดไฟล์สูงสุดใน MB
            quality_preset: คุณภาพการเข้ารหัส (ultrafast, fast, medium, slow, veryslow)
        """
        video_name = Path(video_path).stem
        video_info = self.get_video_info(video_path)
        total_duration = video_info['duration']
        
        if total_duration == 0:
            print(f"❌ ข้ามไฟล์ {video_path} - ไม่สามารถอ่านได้")
            return False
        
        # คำนวณจำนวนส่วนที่ต้องตัด
        num_segments = math.ceil(total_duration / segment_duration)
        
        print(f"\n📹 กำลังประมวลผล: {video_name}")
        print(f"⏱️  ความยาวรวม: {self.format_time(total_duration)} ({total_duration:.1f} วินาที)")
        print(f"📁 ขนาดต้นฉบับ: {video_info['file_size_mb']:.1f} MB")
        print(f"✂️  จะตัดเป็น {num_segments} ส่วน (ส่วนละ {segment_duration} วินาที)")
        print(f"🎯 เป้าหมายขนาดไฟล์: ไม่เกิน {max_size_mb} MB ต่อไฟล์")
        print("-" * 60)
        
        success_count = 0
        
        for i in range(num_segments):
            start_time = i * segment_duration
            actual_duration = min(segment_duration, total_duration - start_time)
            
            # คำนวณ bitrate ที่ต้องการ
            target_bitrate = self.calculate_target_bitrate(actual_duration, max_size_mb)
            
            output_filename = f"{video_name}_part{i+1:03d}.mp4"
            output_path = os.path.join(self.output_folder, output_filename)
            
            print(f"🔄 ส่วนที่ {i+1}/{num_segments}: {output_filename}")
            print(f"   ⏱️  เวลา: {self.format_time(start_time)} - {self.format_time(start_time + actual_duration)}")
            print(f"   📊 Target Bitrate: {target_bitrate//1000}k")
            
            try:
                # ใช้ ffmpeg-python แทน subprocess
                start_time_process = time.time()
                
                # สร้าง ffmpeg pipeline
                stream = ffmpeg.input(video_path, ss=start_time, t=actual_duration)
                stream = ffmpeg.output(
                    stream,
                    output_path,
                    vcodec='libx264',
                    **{
                        'b:v': f"{target_bitrate}",
                        'maxrate': f"{target_bitrate}",
                        'bufsize': f"{target_bitrate * 2}",
                        'c:a': 'aac',
                        'b:a': '128k',
                        'preset': quality_preset,
                        'movflags': '+faststart'
                    }
                )
                
                # รัน ffmpeg แบบเงียบ
                ffmpeg.run(stream, overwrite_output=True, quiet=True)
                
                process_time = time.time() - start_time_process
                
                # ตรวจสอบขนาดไฟล์ที่ได้
                if os.path.exists(output_path):
                    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
                    compression_ratio = (video_info['file_size_mb'] / num_segments) / file_size_mb if file_size_mb > 0 else 0
                    
                    print(f"   ✅ สำเร็จ - ขนาด: {file_size_mb:.1f} MB")
                    print(f"   ⚡ ใช้เวลา: {process_time:.1f} วินาที")
                    print(f"   📉 อัตราบีบอัด: {compression_ratio:.1f}x")
                    
                    if file_size_mb > max_size_mb * 1.1:  # ให้ tolerance 10%
                        print(f"   ⚠️  คำเตือน: ขนาดไฟล์เกินเป้าหมาย ({max_size_mb} MB)")
                    
                    success_count += 1
                else:
                    print(f"   ❌ ไม่พบไฟล์ output")
                    
            except ffmpeg.Error as e:
                print(f"   ❌ ข้อผิดพลาด FFmpeg: ไม่สามารถประมวลผลส่วนที่ {i+1}")
                error_output = e.stderr.decode() if e.stderr else str(e)
                print(f"   📝 รายละเอียด: {error_output[:200]}...")
            except Exception as e:
                print(f"   ❌ ข้อผิดพลาดทั่วไป: {str(e)}")
            
            print()
        
        success_rate = (success_count / num_segments) * 100
        print(f"📊 สรุปการประมวลผล {video_name}:")
        print(f"   ✅ สำเร็จ: {success_count}/{num_segments} ส่วน ({success_rate:.1f}%)")
        
        return success_count == num_segments
    
    def process_all_videos(self, segment_duration: int = 300, max_size_mb: float = 25, 
                          quality_preset: str = "medium") -> dict:
        """
        ประมวลผลวิดีโอทั้งหมด
        
        Args:
            segment_duration: ระยะเวลาการตัดในวินาที
            max_size_mb: ขนาดไฟล์สูงสุดใน MB
            quality_preset: คุณภาพการเข้ารหัส
        """
        video_files = self.get_video_files()
        
        if not video_files:
            print(f"❌ ไม่พบไฟล์วิดีโอในโฟลเดอร์ {self.input_folder}")
            return {'processed': 0, 'failed': 0, 'total': 0}
        
        print("🎬 โปรแกรมตัดและบีบอัดวิดีโอ (ใช้ ffmpeg-python)")
        print("=" * 60)
        print(f"📁 โฟลเดอร์ input: {self.input_folder}")
        print(f"📁 โฟลเดอร์ output: {self.output_folder}")
        print(f"📹 พบไฟล์วิดีโอ: {len(video_files)} ไฟล์")
        print(f"⚙️  ตั้งค่า:")
        print(f"   - ตัดทุก {segment_duration} วินาที ({self.format_time(segment_duration)})")
        print(f"   - ขนาดสูงสุด {max_size_mb} MB ต่อไฟล์")
        print(f"   - คุณภาพ: {quality_preset}")
        print("=" * 60)
        
        processed_count = 0
        failed_count = 0
        total_start_time = time.time()
        
        for idx, video_file in enumerate(video_files, 1):
            print(f"\n🎯 ไฟล์ที่ {idx}/{len(video_files)}: {os.path.basename(video_file)}")
            
            if self.split_and_compress_video(video_file, segment_duration, max_size_mb, quality_preset):
                processed_count += 1
                print(f"✅ ประมวลผลไฟล์ {os.path.basename(video_file)} สำเร็จ")
            else:
                failed_count += 1
                print(f"❌ ประมวลผลไฟล์ {os.path.basename(video_file)} ล้มเหลว")
        
        total_time = time.time() - total_start_time
        
        print("\n" + "=" * 60)
        print("🏁 สรุปการประมวลผลทั้งหมด")
        print("=" * 60)
        print(f"✅ ประมวลผลสำเร็จ: {processed_count} ไฟล์")
        print(f"❌ ประมวลผลล้มเหลว: {failed_count} ไฟล์")
        print(f"📊 รวมทั้งหมด: {len(video_files)} ไฟล์")
        print(f"⏱️  เวลารวม: {self.format_time(total_time)}")
        print(f"📁 ไฟล์ผลลัพธ์อยู่ในโฟลเดอร์: {self.output_folder}")
        
        return {
            'processed': processed_count,
            'failed': failed_count,
            'total': len(video_files),
            'time_taken': total_time
        }

def main():
    parser = argparse.ArgumentParser(description='โปรแกรมตัดและบีบอัดวิดีโอด้วย FFmpeg-Python')
    parser.add_argument('-d', '--duration', type=int, default=300,
                       help='ระยะเวลาการตัดในวินาที (default: 300)')
    parser.add_argument('-s', '--size', type=float, default=25,
                       help='ขนาดไฟล์สูงสุดใน MB (default: 25)')
    parser.add_argument('-q', '--quality', choices=['ultrafast', 'fast', 'medium', 'slow', 'veryslow'],
                       default='medium', help='คุณภาพการเข้ารหัส (default: medium)')
    parser.add_argument('-i', '--input', default='input_vdo',
                       help='โฟลเดอร์ input (default: input_vdo)')
    parser.add_argument('-o', '--output', default='output_vdo',
                       help='โฟลเดอร์ output (default: output_vdo)')
    parser.add_argument('--interactive', action='store_true',
                       help='โหมดโต้ตอบ (ถามค่าจากผู้ใช้)')
    
    args = parser.parse_args()
    
    if args.interactive:
        print("🎬 โปรแกรมตัดและบีบอัดวิดีโอ (โหมดโต้ตอบ)")
        print("=" * 60)
        
        try:
            segment_duration = int(input(f"⏱️  ระบุระยะเวลาการตัด (วินาที) [default: {args.duration}]: ") or args.duration)
            max_size_mb = float(input(f"📦 ระบุขนาดไฟล์สูงสุด (MB) [default: {args.size}]: ") or args.size)
            
            print("\n🎚️  เลือกคุณภาพการเข้ารหัส:")
            print("   1. ultrafast (เร็วที่สุด, คุณภาพต่ำ)")
            print("   2. fast (เร็ว)")
            print("   3. medium (ปกติ) [default]")
            print("   4. slow (ช้า, คุณภาพดี)")
            print("   5. veryslow (ช้าที่สุด, คุณภาพดีที่สุด)")
            
            quality_choice = input("เลือก (1-5): ").strip()
            quality_map = {'1': 'ultrafast', '2': 'fast', '3': 'medium', '4': 'slow', '5': 'veryslow'}
            quality_preset = quality_map.get(quality_choice, args.quality)
            
        except ValueError:
            print("❌ ค่าที่ป้อนไม่ถูกต้อง ใช้ค่าเริ่มต้น")
            segment_duration = args.duration
            max_size_mb = args.size
            quality_preset = args.quality
    else:
        segment_duration = args.duration
        max_size_mb = args.size
        quality_preset = args.quality
    
    try:
        # สร้าง processor และเริ่มประมวลผล
        processor = VideoProcessor(input_folder=args.input, output_folder=args.output)
        result = processor.process_all_videos(segment_duration, max_size_mb, quality_preset)
        
        # บันทึกสรุปผลลงไฟล์
        summary_file = os.path.join(args.output, 'processing_summary.json')
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'settings': {
                    'segment_duration': segment_duration,
                    'max_size_mb': max_size_mb,
                    'quality_preset': quality_preset,
                    'input_folder': args.input,
                    'output_folder': args.output
                },
                'results': result
            }, f, indent=2, ensure_ascii=False)
        
        print(f"📝 สรุปผลการประมวลผลบันทึกในไฟล์: {summary_file}")
        
    except KeyboardInterrupt:
        print("\n⏹️  การประมวลผลถูกยกเลิก")
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")
        raise

if __name__ == "__main__":
    main()
