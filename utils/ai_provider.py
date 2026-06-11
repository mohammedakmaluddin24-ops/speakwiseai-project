OLLAMA_BASE_URL = "http://localhost:11434"


COACHING_PROMPT = """You are an expert public speaking coach. Analyze this speech transcript and provide:

1. Confidence analysis
2. Clarity analysis
3. Speaking strengths
4. Areas for improvement
5. Public speaking tips
6. Overall rating out of 10

Also include:
- Speech summary
- Weakness analysis
- Interview readiness score out of 10
- Public speaking recommendations
- Action plan for improvement

Return structured feedback with clear headings.

Transcript:
{transcript}
"""


def _build_prompt(transcript: str) -> str:
    return COACHING_PROMPT.format(transcript=transcript.strip())


def generate_feedback_with_ollama(transcript: str, model: str = "llama3") -> str:
    try:
        import ollama
    except ImportError as exc:
        raise RuntimeError("The ollama package is not installed. Run pip install ollama.") from exc

    try:
        client = ollama.Client(host=OLLAMA_BASE_URL)
        response = client.chat(
            model=model or "llama3",
            messages=[{"role": "user", "content": _build_prompt(transcript)}],
        )
    except Exception as exc:
        raise RuntimeError("Local AI server not running. Start Ollama and try again.") from exc

    return response.get("message", {}).get("content", "").strip()


def generate_feedback_with_openai(transcript: str, api_key: str, model: str = "gpt-4o-mini") -> str:
    if not api_key:
        raise ValueError("Please enter your API key.")

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("The openai package is not installed. Run pip install openai.") from exc

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a practical, encouraging public speaking coach."},
            {"role": "user", "content": _build_prompt(transcript)},
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content.strip()


def generate_feedback_with_gemini(transcript: str, api_key: str, model: str = "gemini-1.5-flash") -> str:
    if not api_key:
        raise ValueError("Please enter your API key.")

    try:
        import google.generativeai as genai
    except ImportError as exc:
        raise RuntimeError("The google-generativeai package is not installed. Run pip install google-generativeai.") from exc

    genai.configure(api_key=api_key)
    gemini_model = genai.GenerativeModel(model)
    response = gemini_model.generate_content(_build_prompt(transcript))
    return (response.text or "").strip()


def get_ai_feedback(transcript: str, provider: str, api_key: str | None = None, model: str | None = None) -> str:
    if not transcript.strip():
        raise ValueError("Transcript is empty.")

    if provider == "Local AI (Ollama)":
        return generate_feedback_with_ollama(transcript, model or "llama3")
    if provider == "OpenAI API":
        return generate_feedback_with_openai(transcript, api_key or "")
    if provider == "Gemini API":
        return generate_feedback_with_gemini(transcript, api_key or "")

    raise ValueError(f"Unsupported AI provider: {provider}")
