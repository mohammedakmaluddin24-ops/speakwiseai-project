from pathlib import Path
import importlib.util


ROOT_MODULE = Path(__file__).resolve().parents[2] / "utils" / "analysis.py"
spec = importlib.util.spec_from_file_location("speakwise_root_analysis", ROOT_MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

count_fillers = module.count_fillers
calculate_wpm = module.calculate_wpm
total_words = module.total_words
top_words = module.top_words
