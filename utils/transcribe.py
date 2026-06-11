import os
from pathlib import Path
from subprocess import CalledProcessError, run

import imageio_ffmpeg
import numpy as np
import whisper
import whisper.audio


def _configure_bundled_ffmpeg() -> None:
    ffmpeg_path = Path(imageio_ffmpeg.get_ffmpeg_exe())
    os.environ["PATH"] = f"{ffmpeg_path.parent}{os.pathsep}{os.environ.get('PATH', '')}"

    def load_audio_with_bundled_ffmpeg(file: str, sr: int = whisper.audio.SAMPLE_RATE):
        cmd = [
            str(ffmpeg_path),
            "-nostdin",
            "-threads",
            "0",
            "-i",
            file,
            "-f",
            "s16le",
            "-ac",
            "1",
            "-acodec",
            "pcm_s16le",
            "-ar",
            str(sr),
            "-",
        ]
        try:
            out = run(cmd, capture_output=True, check=True).stdout
        except CalledProcessError as exc:
            raise RuntimeError(f"Failed to load audio: {exc.stderr.decode()}") from exc

        return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

    whisper.audio.load_audio = load_audio_with_bundled_ffmpeg
    whisper.load_audio = load_audio_with_bundled_ffmpeg
    whisper.audio.log_mel_spectrogram.__globals__["load_audio"] = load_audio_with_bundled_ffmpeg


def transcribe_audio(audio_path):
    """Transcribe an audio file with the Whisper base model."""
    path = Path(audio_path)
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")

    _configure_bundled_ffmpeg()
    model = whisper.load_model("base")
    result = model.transcribe(str(path))
    return (result.get("text") or "").strip()
