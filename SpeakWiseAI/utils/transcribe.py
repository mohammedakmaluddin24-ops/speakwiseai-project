from pathlib import Path
import importlib.util


ROOT_MODULE = Path(__file__).resolve().parents[2] / "utils" / "transcribe.py"
spec = importlib.util.spec_from_file_location("speakwise_root_transcribe", ROOT_MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

transcribe_audio = module.transcribe_audio
