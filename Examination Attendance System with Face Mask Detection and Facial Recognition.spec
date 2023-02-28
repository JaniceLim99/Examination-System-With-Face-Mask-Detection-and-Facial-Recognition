# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['loading_screen.py'],
    pathex=[],
    binaries=[],
    datas=[('data_classifier_2/*', 'data_classifier_2/'), ('haarcascades/*', 'haarcascades/'), ('images/*', 'images/'), ('student_data/*', 'student_data/'), ('student_mask_data/*', 'student_mask_data/'), ('StudentLabel/*', 'StudentLabel/'), ('examination_facial_demo.sql', '.'), ('db_connection.py', '.'), ('login.py', '.'), ('main_window.py', '.'), ('mark_attendance_bwmask.py', '.'), ('student_detail_page.py', '.'), ('take_picture.py', '.'), ('track_attendance_page.py', '.'), ('loading_screen.py', '.')],
    hiddenimports=['babel.numbers'],
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
    name='Examination Attendance System with Face Mask Detection and Facial Recognition',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='images\\ICON.png',
)
