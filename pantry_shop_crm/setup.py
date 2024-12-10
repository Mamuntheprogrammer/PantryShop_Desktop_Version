import sys
from cx_Freeze import setup, Executable
import os

# Add TCL and TK paths for packaging
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

# Define the executables
executables = [
    Executable(
        'main.py',
        icon="icon.ico",  # Specify the application icon
        base=base
    )
]

# Shortcut table for MSI
shortcut_table = [
    (
        "DesktopShortcut",         # Shortcut
        "DesktopFolder",           # Directory_
        "Pantry Shop",             # Name
        "TARGETDIR",               # Component_
        "[TARGETDIR]main.exe",     # Target (ensure the output name matches)
        None,                      # Arguments
        "Pantry Shop Application", # Description
        None,                      # Hotkey
        "icon.ico",                # Icon
        0,                         # IconIndex
        None,                      # ShowCmd
        "TARGETDIR"                # WkDir
    )
]

# MSI data
msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {'data': msi_data}

# Build options
options = {
    "bdist_msi": bdist_msi_options,
    'build_exe': {
        'include_files': [
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
            'icon.ico'
        ],
        'packages': ['tkcalendar','openpyxl','reportlab','pandas','ttkthemes', 'tkinter','loader','matplotlib',], # Include required packages
    },
}

# Setup configuration
setup(
    name='Pantry Shop',
    version="1.0",
    description='Pantry Shop Application',
    author='UV Project',
    author_email='contact@uvproject.com',  # Replace with a valid email or leave blank
    options=options,
    executables=executables
)
