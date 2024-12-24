# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_data_files, collect_all
from PyInstaller.utils.hooks import copy_metadata

casadi_path = r"C:\Users\User\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\casadi"

# Collect all DLLs from the casadi directory
casadi_dlls = [(os.path.join(casadi_path, file), '.')
               for file in os.listdir(casadi_path) if file.endswith('.dll')]

datas = [("C:\\Users\\User\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python310\\site-packages\\streamlit\\runtime", ".\\streamlit\\runtime")]
datas += collect_data_files("streamlit")
datas += collect_data_files("streamlit_stl", include_py_files=True)
datas += collect_data_files("casadi", include_py_files=True)
datas += copy_metadata("streamlit")
datas += copy_metadata("cadquery")
datas += [('fonts', 'fonts'),
          ('app', 'app')]

a = Analysis(
    ['app\\run.py'],
    pathex=["."],
    binaries=casadi_dlls,
    datas=datas,
    hiddenimports=[
        'casadi',
        'cadquery',
        'OCP',
        'vtk',
        'streamlit_stl',
        'streamlit',
        'os',
        'sys',
        'pathlib',
        'time'
    ],
    hookspath=['.\\hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='TextTango',
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
