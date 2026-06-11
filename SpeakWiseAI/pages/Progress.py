from pathlib import Path
import importlib.util
import sys


ROOT_DIR = Path(__file__).resolve().parents[2]
ROOT_PAGE = ROOT_DIR / "pages" / "Progress.py"

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

spec = importlib.util.spec_from_file_location("speakwise_root_progress", ROOT_PAGE)
progress_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(progress_module)


if __name__ == "__main__":
    progress_module.main()
