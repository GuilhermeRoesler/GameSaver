# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['gamesaver/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('games_database.json', '.'),
        ('gamesaver/gui/styles.qss', 'gamesaver/gui'),
        ('images/icon.png', 'images'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GameSaver',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
