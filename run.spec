# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata

datas = [("/Users/lmonari/anaconda3/envs/3d/lib/python3.12/site-packages/streamlit/runtime", "./streamlit/runtime")]
datas += collect_data_files("streamlit")
datas += copy_metadata("streamlit")
datas += copy_metadata("cadquery")
datas += collect_data_files("streamlit_stl", include_py_files=True)
datas += [('fonts', 'fonts'),
          ('app', 'app'),]


a = Analysis(
    ['app/run.py'],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=['cadquery', 
                   'OCP', 
                   'vtk', 
                   'streamlit_stl',
                   'streamlit', 
                   'os', 
                   'sys', 
                   'pathlib', 
                   'time'],
    hookspath=['./hooks'],
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
    name='run',
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
)
