# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

# เพิ่ม path ปัจจุบัน
block_cipher = None

# รายการไฟล์ที่ต้องการรวม
added_files = [
    ('config.json', '.'),
    ('GUI_GUIDE.md', '.'),
    ('README.md', '.'),
    ('QUICKSTART.md', '.'),
]

# Hidden imports ที่จำเป็น
hidden_imports = [
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'subprocess',
    'threading',
    'pathlib',
    'json',
    'os',
    'time',
    'math',
    'glob'
]

a = Analysis(
    ['video_processor_gui.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='VideoProcessor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI mode
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
    version_file=None,
    manifest=None,
    uac_admin=False,
    uac_uiaccess=False,
)
