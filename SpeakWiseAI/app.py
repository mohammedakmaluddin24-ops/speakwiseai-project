from pathlib import Path
import importlib.util
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
ROOT_APP = ROOT_DIR / "app.py"

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

spec = importlib.util.spec_from_file_location("speakwise_root_app", ROOT_APP)
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)


if __name__ == "__main__":
    app_module.main()
