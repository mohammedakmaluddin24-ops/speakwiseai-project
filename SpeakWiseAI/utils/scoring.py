from pathlib import Path
import importlib.util


ROOT_MODULE = Path(__file__).resolve().parents[2] / "utils" / "scoring.py"
spec = importlib.util.spec_from_file_location("speakwise_root_scoring", ROOT_MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

confidence_score = module.confidence_score
generate_feedback = module.generate_feedback
