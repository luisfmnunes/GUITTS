import whisper
from pathlib import Path

def transcribe_audio(file_path: Path, model_type: str, lang_mode: str) -> tuple[str, dict]:
    model = whisper.load_model(model_type)
    options = {"language": "en"} if lang_mode == "English-only" else {}
    result = model.transcribe(file_path.absolute(), **options)
    return result["text"], result