"""
ตัวตรวจสอบระบบก่อนรันโปรแกรม
"""
import subprocess
import sys
import os
from pathlib import Path

def check_python():
    """ตรวจสอบ Python version"""
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 7:
            print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
            return True
        else:
            print(f"❌ Python version ต่ำเกินไป: {version.major}.{version.minor}")
            print("📥 ต้องการ Python 3.7 ขึ้นไป")
            return False
    except Exception as e:
        print(f"❌ ไม่สามารถตรวจสอบ Python ได้: {e}")
        return False

def check_ffmpeg():
    """ตรวจสอบ FFmpeg"""
    try:
        # ตรวจสอบ ffmpeg
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            # หาเวอร์ชัน
            version_line = result.stdout.split('\n')[0]
            print(f"✓ {version_line}")
            
            # ตรวจสอบ ffprobe
            probe_result = subprocess.run(['ffprobe', '-version'], 
                                        capture_output=True, text=True, timeout=10)
            if probe_result.returncode == 0:
                print("✓ FFprobe พร้อมใช้งาน")
                return True
            else:
                print("❌ ไม่พบ FFprobe")
                return False
        else:
            print("❌ FFmpeg ไม่พร้อมใช้งาน")
            return False
            
    except FileNotFoundError:
        print("❌ ไม่พบ FFmpeg")
        print_ffmpeg_install_guide()
        return False
    except subprocess.TimeoutExpired:
        print("❌ FFmpeg ตอบสนองช้า")
        return False
    except Exception as e:
        print(f"❌ ข้อผิดพลาดในการตรวจสอบ FFmpeg: {e}")
        return False

def print_ffmpeg_install_guide():
    """แสดงวิธีติดตั้ง FFmpeg"""
    print("\n📥 วิธีติดตั้ง FFmpeg:")
    print("1. ดาวน์โหลดจาก: https://ffmpeg.org/download.html")
    print("2. สำหรับ Windows:")
    print("   - ดาวน์โหลด 'Windows builds by BtbN'")
    print("   - แตกไฟล์ไปยัง C:\\ffmpeg")
    print("   - เพิ่ม C:\\ffmpeg\\bin ใน System PATH")
    print("3. ทดสอบ: เปิด Command Prompt แล้วพิมพ์ 'ffmpeg -version'")

def check_dependencies():
    """ตรวจสอบ Python packages"""
    required_packages = ['ffmpeg-python', 'tqdm']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ ไม่พบ {package}")
    
    if missing_packages:
        print(f"\n📦 ติดตั้ง packages ที่ขาด:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_folders():
    """ตรวจสอบและสร้างโฟลเดอร์ที่จำเป็น"""
    folders = ['input_vdo', 'output_vdo']
    
    for folder in folders:
        path = Path(folder)
        if not path.exists():
            path.mkdir(exist_ok=True)
            print(f"📁 สร้างโฟลเดอร์: {folder}")
        else:
            print(f"✓ โฟลเดอร์ {folder} พร้อมใช้งาน")
    
    return True

def check_video_files():
    """ตรวจสอบไฟล์วิดีโอใน input folder"""
    input_folder = Path('input_vdo')
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v']
    
    video_files = []
    for ext in video_extensions:
        video_files.extend(input_folder.glob(f'*{ext}'))
        video_files.extend(input_folder.glob(f'*{ext.upper()}'))
    
    if video_files:
        print(f"📹 พบไฟล์วิดีโอ: {len(video_files)} ไฟล์")
        for video in video_files[:5]:  # แสดงแค่ 5 ไฟล์แรก
            size_mb = video.stat().st_size / (1024 * 1024)
            print(f"   - {video.name} ({size_mb:.1f} MB)")
        if len(video_files) > 5:
            print(f"   ... และอีก {len(video_files) - 5} ไฟล์")
    else:
        print("⚠️  ไม่พบไฟล์วิดีโอใน input_vdo/")
        print("📥 กรุณาวางไฟล์วิดีโอใน input_vdo/ ก่อนรันโปรแกรม")
    
    return len(video_files) > 0

def main():
    """ตรวจสอบระบบทั้งหมด"""
    print("🔍 ตรวจสอบความพร้อมของระบบ")
    print("=" * 50)
    
    checks = [
        ("Python", check_python),
        ("FFmpeg", check_ffmpeg),
        ("Python Packages", check_dependencies),
        ("โฟลเดอร์", check_folders),
        ("ไฟล์วิดีโอ", check_video_files)
    ]
    
    all_good = True
    
    for name, check_func in checks:
        print(f"\n🔎 ตรวจสอบ {name}:")
        if not check_func():
            all_good = False
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 ระบบพร้อมใช้งาน!")
        print("🚀 สามารถรันโปรแกรมได้แล้ว:")
        print("   python video_processor.py --interactive")
    else:
        print("⚠️  พบปัญหาบางอย่าง กรุณาแก้ไขก่อนใช้งาน")
    
    return all_good

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  การตรวจสอบถูกยกเลิก")
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")
        
    input("\nกดปุ่ม Enter เพื่อปิด...")
