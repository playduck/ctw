# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import os
import sys
import importlib

name = "ctw-core"

print("Platform: ", sys.platform)
print("Path: ", os.path.abspath("./src/main.py"))

block_cipher = None
hiddenimports=[
]

a = Analysis([os.path.abspath("./src/main.py")],
            pathex=[os.path.abspath("./")],
            binaries=[],
            datas=[],
            hiddenimports=hiddenimports,
            hookspath=[],
            runtime_hooks=[],
            excludes=[],
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            cipher=block_cipher,
            noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data,
            cipher=block_cipher)

if sys.platform == "darwin":
    exe = EXE(pyz,
            a.scripts,
            name=name,
            exclude_binaries=True,
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            runtime_tmpdir=None,
            console=True,
            icon=None
)
elif sys.platform == "win32" or sys.platform == "win64" or sys.platform == "linux":
    exe = EXE(pyz,
            a.scripts,
            # a.binaries,
            # a.zipfiles,
            # a.datas,
            name=name,
            exclude_binaries=True,
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            runtime_tmpdir=None,
            console=True,
            icon=None
)
else:
    print("No Target for ", sys.platform)
    sys.exit(1)


if sys.platform == "darwin":
    coll = COLLECT(exe,
            a.binaries,
            a.zipfiles,
            a.datas,
            strip=False,
            upx=True,
            upx_exclude=[],
            name=name
    )
    app = BUNDLE(exe,
            a.binaries,
            a.zipfiles,
            a.datas,
            name=name+".app",
            info_plist={
                "NSHighResolutionCapable": "True",
                "LSBackgroundOnly": "False",
                "NSRequiresAquaSystemAppearance": "True"
                # should be false to support dark mode
                # known bug: https://github.com/pyinstaller/pyinstaller/issues/4615 with pyinstaller
            },
            icon=None
    )

elif sys.platform == "win32" or sys.platform == "win64":
    coll = COLLECT(exe,
                a.binaries,
                a.zipfiles,
                a.datas,
                strip=False,
                upx=True,
                upx_exclude=[],
                name=name
    )
