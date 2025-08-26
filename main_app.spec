# main.spec

import sys
from PyInstaller.utils.hooks import collect_all

# Increase recursion limit for large PySide6 apps
sys.setrecursionlimit(sys.getrecursionlimit() * 5)

# Initialize resource lists
datas = []
binaries = []
hiddenimports = []

# Collect necessary modules
for module in ['primer3', 'openpyxl', 'pandas', 'Bio', 'PySide6', 'matplotlib', 'numpy']:
    collected = collect_all(module)
    datas += collected[0]
    binaries += collected[1]
    hiddenimports += collected[2]

# Add additional hidden imports manually
hiddenimports += [
    'primer3.bindings',
    'primer3',
    'verano.design',
    'xlsxwriter'
]

# Add extra data folders and binaries (preserving relative structure)
datas += [
    ('src', 'src'),  # Your app source code
    ('tools', 'tools'),
    ('tools/dimond/diamond.exe', 'tools/dimond'),
    ('data', 'data'),
    ('src/R', 'src/R')
]

# Start Analysis block
a = Analysis(
    ['src\\main_app.py'],
    pathex=['src'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={
        'matplotlib': {'backends': ['Agg']}
    },
    runtime_hooks=[],
    excludes=[
        'PyQt6', 'PyQt5', 'tkinter', 'sphinx', 'IPython', 'pytest', 'scipy', 'pyarrow',
        'PySide6.Qt3DAnimation', 'PySide6.Qt3DCore', 'PySide6.Qt3DExtras', 'PySide6.Qt3DInput',
        'PySide6.Qt3DLogic', 'PySide6.Qt3DRender', 'PySide6.QtAxContainer', 'PySide6.QtBluetooth',
        'PySide6.QtCharts', 'PySide6.QtConcurrent', 'PySide6.QtDataVisualization', 'PySide6.QtDBus',
        'PySide6.QtDesigner', 'PySide6.QtGraphs', 'PySide6.QtHelp', 'PySide6.QtHttpServer',
        'PySide6.QtLocation', 'PySide6.QtMultimedia', 'PySide6.QtMultimediaWidgets',
        'PySide6.QtNetworkAuth', 'PySide6.QtNfc', 'PySide6.QtOpenGL', 'PySide6.QtOpenGLWidgets',
        'PySide6.QtPdf', 'PySide6.QtPdfWidgets', 'PySide6.QtPositioning', 'PySide6.QtPrintSupport',
        'PySide6.QtQuick', 'PySide6.QtQuick3D', 'PySide6.QtQuickControls2', 'PySide6.QtQuickWidgets',
        'PySide6.QtRemoteObjects', 'PySide6.QtScxml', 'PySide6.QtSensors', 'PySide6.QtSerialBus',
        'PySide6.QtSerialPort', 'PySide6.QtSpatialAudio', 'PySide6.QtSql', 'PySide6.QtStateMachine',
        'PySide6.QtSvg', 'PySide6.QtSvgWidgets', 'PySide6.QtTest', 'PySide6.QtTextToSpeech',
        'PySide6.QtUiTools', 'PySide6.QtWebChannel', 'PySide6.QtWebEngineCore', 'PySide6.QtWebEngineQuick',
        'PySide6.QtWebEngineWidgets', 'PySide6.QtWebSockets', 'PySide6.QtXml'
    ],
    noarchive=False,
    optimize=0,
)

# Package into Python archive
pyz = PYZ(a.pure)

# Build the executable
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GenomeWideWorkBench',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Change to False if you want no console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src\\image.ico',
)

# Final collection
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=['Rscript.exe'],  # Optional: prevent compressing this if used
    name='GenomeWideWorkBench',
)
