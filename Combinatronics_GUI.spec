# -*- mode: python ; coding: utf-8 -*-

import geopandas
import os

block_cipher = None

a = Analysis(['Combinatronics_GUI.py'],
             pathex=[os.path.dirname(geopandas.__file__)],
             binaries=[],
             datas=[(r'C:\Users\dylow\gdal-3.9.2', '.')],
             hiddenimports=['geopandas', 'fiona'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='Combinatronics_GUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Combinatronics_GUI')