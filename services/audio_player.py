from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl

from pathlib import Path

class AudioPlayer:
    def __init__(self):
        self.player = QMediaPlayer()
        self.output = QAudioOutput()
        self.player.setAudioOutput(self.output)

    def load(self, path: Path):
        self.player.setSource(QUrl.fromLocalFile(path.absolute()))
    
    def play(self):
        self.player.play()