import whisper
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from pathlib import Path

class TranscriptionWorker(QObject):
    finished = pyqtSignal(str, dict)
    error = pyqtSignal(str)

    def __init__(self, file_path: Path, model_type: str, lang_mode: str):
        super().__init__()
        self.audio_path = file_path
        self._model_type = None
        self._lang_mode = None

        self.model = None
        self.set_model(model_type)
        self.set_lang_mode(lang_mode)
        

    def run(self) -> None:
        try:
            result = self.model.transcribe(self.audio_path.absolute().as_posix(), **self.options)
            self.finished.emit(result["text"], result)
        except Exception as e:
            self.error.emit(str(e))
    
    def set_model(self, model_type: str) -> None:
        if self._model_type == model_type:
            return
        self._model_type = model_type
        self.model = whisper.load_model(model_type)

    def set_lang_mode(self, lang_mode: str) -> None:
        if self._lang_mode == lang_mode:
            return
        self._lang_mode = lang_mode
        self.options = {"language": "en"} if lang_mode == "English-only" else {}


def transcribe_audio(file_path: Path, model_type: str, lang_mode: str) -> tuple[str, dict]:
    model = whisper.load_model(model_type)
    options = {"language": "en"} if lang_mode == "English-only" else {}
    result = model.transcribe(file_path.absolute().as_posix(), **options)
    return result["text"], result