# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    [
    'gui.py'
    ],
    # 打包项目路径
    pathex=['/Users/yuanmoc/Documents/py-workspace/health-160'],
    binaries=[],
    # 第三方资源文件，默认不会添加进来，要手动添加
    datas=[
        ('package/app/ui/main-ui.ui', 'app/ui'),
        ('package/app/ui/login-ui.ui', 'app/ui')
    ],
    # 引入的包
    hiddenimports=[
        'utils',
        'app',
        'utils.qt6',
        'utils.qt6.search_combo_box',
        'utils.qt6.multi_select_combo_box',
        'PIL'
    ],
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
    [],
    exclude_binaries=True,
    name='HealthMate',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    # 启动时显示命令行
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='HealthMate',
)
app = BUNDLE(
    coll,
    name='HealthMate.app',
    icon='img/favicon.ico',
    bundle_identifier=None,
)
