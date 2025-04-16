import sys
import os
import subprocess
import shutil
from PyQt6.QtWidgets import QMessageBox

def ensure_ffmpeg(parent=None):
    if shutil.which("ffmpeg"):
        return
    
    QMessageBox.information(parent, "Installing ffmpeg", "ffmpeg is not installed. Attempting to install...")
    if sys.platform.startswith("linux"):
        subprocess.run(["sudo", "apt", "install", "ffmpeg", "-y"])
    elif sys.platform.startswith("darwin"):
        subprocess.run(["brew", "install", "ffmpeg"])
    elif sys.platform.startswith("win"):
        QMessageBox.critical(parent, "Missing ffmpeg", "Please install ffmpeg before running the application.")
    else:
        QMessageBox.critical(parent, "Unsupported OS", "Your operating system is not supported. Please install ffmpeg manually.")