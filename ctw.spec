# -*- mode: python -*-

from pathlib import Path
import os
import sys
import importlib

block_cipher = None
hiddenimports=["pkg_resources"]

a = Analysis(["./src/main.py"],
            pathex=[os.path.abspath("./")],
            binaries=None,
            datas=None,
            hiddenimports=hiddenimports,
            hookspath=None,
            runtime_hooks=None,
            excludes=None,
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            cipher=block_cipher,
            noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
            cipher=block_cipher)

if sys.platform == "darwin":
    exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            name="ctw",
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            runtime_tmpdir=None,
            console=False,
            icon=None
    )
elif sys.platform == "win32" or sys.platform == "win64" or sys.platform == "linux":
    exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            name="ctw",
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            runtime_tmpdir=None,
            console=False,
            icon=None
)

if sys.platform == "darwin":
    app = BUNDLE(exe,
                    name="ctw.app",
                    info_plist={
                        "NSHighResolutionCapable": "True",
                        "LSBackgroundOnly": "False",
                        "NSRequiresAquaSystemAppearance": "True"
                        # should be false to support dark mode
                        # known bug: https://github.com/pyinstaller/pyinstaller/issues/4615 with pyinstaller
                        # need to recompile pyinstaller with SDK >= 10.13
                    },
                    icon=None
                    )
