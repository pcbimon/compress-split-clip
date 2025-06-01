import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import subprocess
import math
import time
from pathlib import Path
import json
from typing import Optional
import webbrowser

class VideoProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 โปรแกรมตัดและบีบอัดวิดีโอ")
        self.root.geometry("700x650")
        self.root.resizable(True, True)
        
        # ตัวแปรสำหรับเก็บค่า
        self.source_file = tk.StringVar()
        self.output_folder = "output_vdo"
        self.file_size = tk.DoubleVar(value=25.0)
        self.duration_value = tk.IntVar(value=300)
        self.duration_unit = tk.StringVar(value="วินาที")
        self.quality_preset = tk.StringVar(value="medium")
        self.is_processing = False
        
        # สร้าง output folder
        Path(self.output_folder).mkdir(exist_ok=True)
        
        self.setup_ui()
        self.check_ffmpeg()
    
    def setup_ui(self):
        """สร้าง UI หลัก"""
        # หัวข้อหลัก
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill="x", padx=10, pady=5)
        
        title_label = ttk.Label(title_frame, text="🎬 โปรแกรมตัดและบีบอัดวิดีโอ", 
                               font=("Arial", 16, "bold"))
        title_label.pack()
        
        # Frame หลักสำหรับการตั้งค่า
        main_frame = ttk.LabelFrame(self.root, text="การตั้งค่า", padding=10)
        main_frame.pack(fill="x", padx=10, pady=5)
        
        # 1. เลือกไฟล์ต้นฉบับ
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill="x", pady=5)
        
        ttk.Label(file_frame, text="Select Source File:", font=("Arial", 10, "bold")).pack(anchor="w")
        
        file_select_frame = ttk.Frame(file_frame)
        file_select_frame.pack(fill="x", pady=2)
        
        self.file_entry = ttk.Entry(file_select_frame, textvariable=self.source_file, 
                                   font=("Arial", 9))
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ttk.Button(file_select_frame, text="เลือกไฟล์", 
                  command=self.select_file).pack(side="right")
        
        # 2. ขนาดไฟล์
        size_frame = ttk.Frame(main_frame)
        size_frame.pack(fill="x", pady=5)
        
        ttk.Label(size_frame, text="ขนาดไฟล์สูงสุด (MB):", font=("Arial", 10, "bold")).pack(anchor="w")
        
        size_input_frame = ttk.Frame(size_frame)
        size_input_frame.pack(fill="x", pady=2)
        
        size_spinbox = ttk.Spinbox(size_input_frame, from_=1, to=1000, 
                                  textvariable=self.file_size, width=10)
        size_spinbox.pack(side="left")
        
        ttk.Label(size_input_frame, text="MB").pack(side="left", padx=(5, 0))
        
        # ปุ่มขนาดที่แนะนำ
        size_preset_frame = ttk.Frame(size_input_frame)
        size_preset_frame.pack(side="right")
        
        ttk.Button(size_preset_frame, text="10 MB (SNS)", width=12,
                  command=lambda: self.file_size.set(10)).pack(side="left", padx=2)
        ttk.Button(size_preset_frame, text="25 MB (YouTube)", width=12,
                  command=lambda: self.file_size.set(25)).pack(side="left", padx=2)
        ttk.Button(size_preset_frame, text="100 MB (Archive)", width=12,
                  command=lambda: self.file_size.set(100)).pack(side="left", padx=2)
        
        # 3. ระยะเวลาการแบ่ง
        duration_frame = ttk.Frame(main_frame)
        duration_frame.pack(fill="x", pady=5)
        
        ttk.Label(duration_frame, text="ระยะเวลาการแบ่ง:", font=("Arial", 10, "bold")).pack(anchor="w")
        
        duration_input_frame = ttk.Frame(duration_frame)
        duration_input_frame.pack(fill="x", pady=2)
        
        duration_spinbox = ttk.Spinbox(duration_input_frame, from_=1, to=3600, 
                                      textvariable=self.duration_value, width=10)
        duration_spinbox.pack(side="left")
        
        # หน่วยเวลา
        unit_combo = ttk.Combobox(duration_input_frame, textvariable=self.duration_unit,
                                 values=["วินาที", "นาที"], state="readonly", width=8)
        unit_combo.pack(side="left", padx=(5, 0))
        unit_combo.bind("<<ComboboxSelected>>", self.on_unit_change)
        
        # ปุ่มเวลาที่แนะนำ
        duration_preset_frame = ttk.Frame(duration_input_frame)
        duration_preset_frame.pack(side="right")
        
        ttk.Button(duration_preset_frame, text="30 วิ (SNS)", width=12,
                  command=lambda: self.set_duration(30, "วินาที")).pack(side="left", padx=2)
        ttk.Button(duration_preset_frame, text="5 นาที", width=12,
                  command=lambda: self.set_duration(5, "นาที")).pack(side="left", padx=2)
        ttk.Button(duration_preset_frame, text="10 นาที", width=12,
                  command=lambda: self.set_duration(10, "นาที")).pack(side="left", padx=2)
        
        # 4. คุณภาพ
        quality_frame = ttk.Frame(main_frame)
        quality_frame.pack(fill="x", pady=5)
        
        ttk.Label(quality_frame, text="คุณภาพการเข้ารหัส:", font=("Arial", 10, "bold")).pack(anchor="w")
        
        quality_input_frame = ttk.Frame(quality_frame)
        quality_input_frame.pack(fill="x", pady=2)
        
        quality_combo = ttk.Combobox(quality_input_frame, textvariable=self.quality_preset,
                                    values=["ultrafast", "fast", "medium", "slow", "veryslow"],
                                    state="readonly", width=15)
        quality_combo.pack(side="left")
        
        # คำอธิบายคุณภาพ
        quality_desc = {
            "ultrafast": "เร็วที่สุด, คุณภาพต่ำ",
            "fast": "เร็ว, คุณภาพปกติ", 
            "medium": "ปกติ, สมดุล (แนะนำ)",
            "slow": "ช้า, คุณภาพดี",
            "veryslow": "ช้าที่สุด, คุณภาพดีที่สุด"
        }
        
        self.quality_desc_label = ttk.Label(quality_input_frame, 
                                           text=quality_desc[self.quality_preset.get()],
                                           foreground="gray")
        self.quality_desc_label.pack(side="left", padx=(10, 0))
        
        quality_combo.bind("<<ComboboxSelected>>", 
                          lambda e: self.quality_desc_label.config(
                              text=quality_desc[self.quality_preset.get()]))
        
        # ปุ่มดำเนินการ
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        self.process_button = ttk.Button(button_frame, text="🚀 เริ่มประมวลผล", 
                                        command=self.start_processing)
        self.process_button.pack(side="left", padx=(0, 5))
        
        self.stop_button = ttk.Button(button_frame, text="⏹️ หยุด", 
                                     command=self.stop_processing, state="disabled")
        self.stop_button.pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="📁 เปิดโฟลเดอร์ output", 
                  command=self.open_output_folder).pack(side="right")
        
        # Progress bar
        progress_frame = ttk.Frame(self.root)
        progress_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(progress_frame, text="ความคืบหน้า:").pack(anchor="w")
        self.progress = ttk.Progressbar(progress_frame, mode="indeterminate")
        self.progress.pack(fill="x", pady=2)
        
        # พื้นที่แสดงผล (Log)
        log_frame = ttk.LabelFrame(self.root, text="ผลการประมวลผล", padding=5)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, 
                                                 font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True)
        
        # สถานะ FFmpeg
        self.status_label = ttk.Label(self.root, text="กำลังตรวจสอบ FFmpeg...", 
                                     foreground="orange")
        self.status_label.pack(anchor="w", padx=10, pady=2)
    
    def log(self, message):
        """แสดงข้อความใน log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")
        self.root.update_idletasks()
    
    def select_file(self):
        """เลือกไฟล์วิดีโอ"""
        filetypes = [
            ("ไฟล์วิดีโอ", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v"),
            ("MP4 files", "*.mp4"),
            ("AVI files", "*.avi"),
            ("MOV files", "*.mov"),
            ("ไฟล์ทั้งหมด", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="เลือกไฟล์วิดีโอ",
            filetypes=filetypes
        )
        
        if filename:
            self.source_file.set(filename)
            self.log(f"เลือกไฟล์: {os.path.basename(filename)}")
            
            # แสดงข้อมูลไฟล์
            self.show_file_info(filename)
    
    def show_file_info(self, filename):
        """แสดงข้อมูลไฟล์"""
        try:
            file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
            self.log(f"ขนาดไฟล์: {file_size:.1f} MB")
            
            # ถ้ามี FFmpeg ให้แสดงข้อมูลเพิ่มเติม
            if hasattr(self, 'ffmpeg_available') and self.ffmpeg_available:
                self.get_video_duration(filename)
                
        except Exception as e:
            self.log(f"ไม่สามารถอ่านข้อมูลไฟล์ได้: {e}")
    
    def get_video_duration(self, filename):
        """หาความยาวของวิดีโอ"""
        try:
            cmd = [
                'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1', filename
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and result.stdout.strip():
                duration = float(result.stdout.strip())
                minutes = int(duration // 60)
                seconds = int(duration % 60)
                self.log(f"ความยาววิดีโอ: {minutes:02d}:{seconds:02d} นาที")
                
                # คำนวณจำนวนส่วนที่จะได้
                segment_duration = self.get_duration_in_seconds()
                num_segments = math.ceil(duration / segment_duration)
                self.log(f"จะแบ่งเป็น: {num_segments} ส่วน")
                
        except Exception as e:
            self.log(f"ไม่สามารถอ่านความยาววิดีโอได้: {e}")
    
    def set_duration(self, value, unit):
        """ตั้งค่าระยะเวลา"""
        self.duration_value.set(value)
        self.duration_unit.set(unit)
        self.log(f"ตั้งค่าระยะเวลา: {value} {unit}")
    
    def on_unit_change(self, event=None):
        """เมื่อเปลี่ยนหน่วยเวลา"""
        current_value = self.duration_value.get()
        current_unit = self.duration_unit.get()
        self.log(f"เปลี่ยนหน่วยเวลาเป็น: {current_value} {current_unit}")
    
    def get_duration_in_seconds(self):
        """แปลงระยะเวลาเป็นวินาที"""
        value = self.duration_value.get()
        unit = self.duration_unit.get()
        
        if unit == "นาที":
            return value * 60
        else:  # วินาที
            return value
    
    def check_ffmpeg(self):
        """ตรวจสอบ FFmpeg"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.ffmpeg_available = True
                self.status_label.config(text="✓ FFmpeg พร้อมใช้งาน", foreground="green")
                self.log("✓ FFmpeg พร้อมใช้งาน")
            else:
                self.ffmpeg_not_available()
        except Exception:
            self.ffmpeg_not_available()
    
    def ffmpeg_not_available(self):
        """เมื่อไม่พบ FFmpeg"""
        self.ffmpeg_available = False
        self.status_label.config(text="❌ ไม่พบ FFmpeg", foreground="red")
        self.log("❌ ไม่พบ FFmpeg")
        self.log("📥 กรุณาติดตั้ง FFmpeg จาก https://ffmpeg.org/download.html")
        self.process_button.config(state="disabled")
    
    def validate_inputs(self):
        """ตรวจสอบข้อมูลที่ป้อน"""
        if not self.source_file.get():
            messagebox.showerror("ข้อผิดพลาด", "กรุณาเลือกไฟล์วิดีโอ")
            return False
        
        if not os.path.exists(self.source_file.get()):
            messagebox.showerror("ข้อผิดพลาด", "ไฟล์ที่เลือกไม่มีอยู่")
            return False
        
        if not self.ffmpeg_available:
            messagebox.showerror("ข้อผิดพลาด", "ไม่พบ FFmpeg\nกรุณาติดตั้ง FFmpeg ก่อนใช้งาน")
            return False
        
        if self.file_size.get() <= 0:
            messagebox.showerror("ข้อผิดพลาด", "ขนาดไฟล์ต้องมากกว่า 0")
            return False
        
        if self.duration_value.get() <= 0:
            messagebox.showerror("ข้อผิดพลาด", "ระยะเวลาต้องมากกว่า 0")
            return False
        
        return True
    
    def start_processing(self):
        """เริ่มประมวลผล"""
        if not self.validate_inputs():
            return
        
        self.is_processing = True
        self.process_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.progress.start()
        
        # ล้าง log
        self.log_text.delete("1.0", "end")
        
        # เริ่ม thread สำหรับประมวลผล
        self.process_thread = threading.Thread(target=self.process_video, daemon=True)
        self.process_thread.start()
    
    def stop_processing(self):
        """หยุดการประมวลผล"""
        self.is_processing = False
        self.log("⏹️ กำลังหยุดการประมวลผล...")
    
    def process_video(self):
        """ประมวลผลวิดีโอ (รันใน thread แยก)"""
        try:
            video_path = self.source_file.get()
            video_name = Path(video_path).stem
            segment_duration = self.get_duration_in_seconds()
            max_size_mb = self.file_size.get()
            quality_preset = self.quality_preset.get()
            
            self.log(f"🎬 เริ่มประมวลผล: {os.path.basename(video_path)}")
            self.log(f"⚙️ ตั้งค่า:")
            self.log(f"   - แบ่งทุก {segment_duration} วินาที")
            self.log(f"   - ขนาดสูงสุด {max_size_mb} MB")
            self.log(f"   - คุณภาพ: {quality_preset}")
            self.log("-" * 50)
            
            # หาข้อมูลวิดีโอ
            video_info = self.get_video_info(video_path)
            total_duration = video_info['duration']
            
            if total_duration <= 0:
                self.log("❌ ไม่สามารถอ่านข้อมูลวิดีโอได้")
                return
            
            # คำนวณจำนวนส่วน
            num_segments = math.ceil(total_duration / segment_duration)
            
            self.log(f"📊 ข้อมูลวิดีโอ:")
            self.log(f"   - ความยาว: {self.format_time(total_duration)}")
            self.log(f"   - ขนาดต้นฉบับ: {video_info['file_size_mb']:.1f} MB")
            self.log(f"   - จำนวนส่วน: {num_segments}")
            self.log("-" * 50)
            
            success_count = 0
            
            for i in range(num_segments):
                if not self.is_processing:
                    self.log("⏹️ การประมวลผลถูกยกเลิก")
                    break
                
                start_time = i * segment_duration
                actual_duration = min(segment_duration, total_duration - start_time)
                
                output_filename = f"{video_name}_part{i+1:03d}.mp4"
                output_path = os.path.join(self.output_folder, output_filename)
                
                self.log(f"🔄 ส่วนที่ {i+1}/{num_segments}: {output_filename}")
                
                if self.process_segment(video_path, output_path, start_time, 
                                      actual_duration, max_size_mb, quality_preset):
                    success_count += 1
                    self.log(f"   ✅ สำเร็จ")
                else:
                    self.log(f"   ❌ ล้มเหลว")
            
            self.log("-" * 50)
            self.log(f"🏁 เสร็จสิ้น: {success_count}/{num_segments} ส่วน")
            
            if success_count > 0:
                self.log(f"📁 ไฟล์ผลลัพธ์ใน: {self.output_folder}")
                
                # เปิดโฟลเดอร์ output
                self.root.after(1000, self.open_output_folder)
            
        except Exception as e:
            self.log(f"❌ เกิดข้อผิดพลาด: {e}")
        finally:
            # คืนค่า UI
            self.root.after(0, self.processing_finished)
    
    def get_video_info(self, video_path):
        """หาข้อมูลวิดีโอ"""
        try:
            # หาความยาว
            duration_cmd = [
                'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1', video_path
            ]
            duration_result = subprocess.run(duration_cmd, capture_output=True, 
                                           text=True, check=True, timeout=30)
            duration = float(duration_result.stdout.strip()) if duration_result.stdout.strip() else 0
            
            # ขนาดไฟล์
            file_size = os.path.getsize(video_path)
            file_size_mb = file_size / (1024 * 1024)
            
            return {
                'duration': duration,
                'file_size_bytes': file_size,
                'file_size_mb': file_size_mb
            }
        except Exception as e:
            self.log(f"ไม่สามารถอ่านข้อมูลไฟล์ได้: {e}")
            return {'duration': 0, 'file_size_bytes': 0, 'file_size_mb': 0}
    
    def calculate_target_bitrate(self, duration_seconds, max_size_mb):
        """คำนวณ bitrate เป้าหมาย"""
        if duration_seconds <= 0:
            return 1000000
        
        max_size_bits = max_size_mb * 8 * 1024 * 1024
        target_bitrate = int(max_size_bits / duration_seconds)
        return max(int(target_bitrate * 0.75), 100000)  # ลด 25% สำหรับความปลอดภัย
    
    def process_segment(self, video_path, output_path, start_time, duration, max_size_mb, quality_preset):
        """ประมวลผลส่วนหนึ่งของวิดีโอ"""
        try:
            target_bitrate = self.calculate_target_bitrate(duration, max_size_mb)
            
            cmd = [
                'ffmpeg', '-y',
                '-i', video_path,
                '-ss', str(start_time),
                '-t', str(duration),
                '-c:v', 'libx264',
                '-b:v', f"{target_bitrate}",
                '-maxrate', f"{target_bitrate}",
                '-bufsize', f"{target_bitrate * 2}",
                '-c:a', 'aac',
                '-b:a', '128k',
                '-preset', quality_preset,
                '-movflags', '+faststart',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, 
                                  check=True, timeout=300)  # timeout 5 นาที
            
            # ตรวจสอบผลลัพธ์
            if os.path.exists(output_path):
                file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
                self.log(f"   📦 ขนาด: {file_size_mb:.1f} MB")
                return True
            else:
                return False
                
        except subprocess.CalledProcessError as e:
            self.log(f"   ❌ FFmpeg error: {e}")
            return False
        except subprocess.TimeoutExpired:
            self.log(f"   ❌ Timeout")
            return False
        except Exception as e:
            self.log(f"   ❌ Error: {e}")
            return False
    
    def format_time(self, seconds):
        """แปลงวินาทีเป็น HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def processing_finished(self):
        """เมื่อประมวลผลเสร็จสิ้น"""
        self.is_processing = False
        self.progress.stop()
        self.process_button.config(state="normal")
        self.stop_button.config(state="disabled")
    
    def open_output_folder(self):
        """เปิดโฟลเดอร์ output"""
        try:
            output_path = os.path.abspath(self.output_folder)
            if os.path.exists(output_path):
                os.startfile(output_path)  # Windows
                self.log(f"📁 เปิดโฟลเดอร์: {output_path}")
            else:
                self.log("❌ ไม่พบโฟลเดอร์ output")
        except Exception as e:
            self.log(f"❌ ไม่สามารถเปิดโฟลเดอร์ได้: {e}")

def main():
    """รันโปรแกรม"""
    root = tk.Tk()
    app = VideoProcessorGUI(root)
    
    # ปิดโปรแกรมอย่างปลอดภัย
    def on_closing():
        if app.is_processing:
            if messagebox.askokcancel("ออกจากโปรแกรม", 
                                     "กำลังประมวลผลอยู่ ต้องการออกจากโปรแกรมหรือไม่?"):
                app.is_processing = False
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
