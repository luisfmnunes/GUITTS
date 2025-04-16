from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QApplication, QProgressDialog
from PyQt6.QtCore import QUrl, Qt, QThread
from services.audio_player import AudioPlayer
from services.transcription import TranscriptionWorker
from utils.ffmpeg import ensure_ffmpeg

from pathlib import Path

class WhisperApp(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("gui/whisper_gui.ui", self)

        self.audio_path = None
        self.output_path = None

        self.audio_player = AudioPlayer()
        self.worker = None
        ensure_ffmpeg(self)

        self.loadButton.clicked.connect(self.load_audio_file)
        self.previewButton.clicked.connect(self.play_preview)
        self.outputButton.clicked.connect(self.select_output_file)
        self.transcribeButton.clicked.connect(self.transcribe_audio_file)

        self.modelCombo.addItems(["tiny", "base", "small", "medium", "large", "turbo"])
        self.langCombo.addItems(["English-only", "Multilingual"])

    def load_audio_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.m4a *.ogg *.flac)")
        if path:
            self.audio_path = Path(path)
            self.audio_player.load(self.audio_path)
            QMessageBox.information(self, "File Successfuly Loaded", f"Loaded File: {self.audio_path.name}")
        
        if self.worker is not None:
            self.worker.audio_path = self.audio_path

    def play_preview(self):
        if self.audio_path:
            self.audio_player.play()
        else:
            QMessageBox.warning(self, "No File Loaded", "Please load an audio file first.")
    
    def select_output_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Select Output File", "", "Text Files (*.txt)")
        if path:
            self.output_path = Path(path)
    
    def transcribe_audio_file(self):
        if not self.audio_path:
            QMessageBox.warning(self, "No File Loaded", "Please load an audio file first.")
            return
        
        model = self.modelCombo.currentText()
        lang = self.langCombo.currentText()

        if not self.worker:
            self.worker = TranscriptionWorker(self.audio_path, model, lang)
        else:
            self.worker.set_model(model)
            self.worker.set_lang_mode(lang)

        if not self.output_path:
            self.select_output_file()
        
        self.progress = QProgressDialog("Transcribing audio...", None, 0, 0, self)
        self.progress.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.progress.setMinimumDuration(0)
        self.progress.setCancelButton(None)
        self.progress.setWindowTitle("Transcribing Audio")
        self.progress.show()

        self.process = QThread()
        self.worker.moveToThread(self.process)

        self.process.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_transcription_finished)
        self.worker.error.connect(self.on_transcription_error)
        self.worker.finished.connect(self.process.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.process.finished.connect(self.process.deleteLater)

        self.process.start()

    def on_transcription_finished(self, text, result):
        self.progress.close()
        self.output_path.write_text(text)

        QMessageBox.information(self, "Success", f"Transcription saved to {self.output_path}")

    def on_transcription_error(self, error_msg):
        self.progress.close()
        QMessageBox.critical(self, "Error", f"An error occurred during transcription: {error_msg}")
        
