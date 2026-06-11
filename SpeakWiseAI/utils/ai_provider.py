from pathlib import Path
import importlib.util


ROOT_MODULE = Path(__file__).resolve().parents[2] / "utils" / "ai_provider.py"
spec = importlib.util.spec_from_file_location("speakwise_root_ai_provider", ROOT_MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

generate_feedback_with_ollama = module.generate_feedback_with_ollama
generate_feedback_with_openai = module.generate_feedback_with_openai
generate_feedback_with_gemini = module.generate_feedback_with_gemini
get_ai_feedback = module.get_ai_feedback
