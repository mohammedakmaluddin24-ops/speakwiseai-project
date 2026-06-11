import re
import tempfile
import warnings
from pathlib import Path
from subprocess import CalledProcessError, run

import imageio_ffmpeg
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from pydub import AudioSegment
from wordcloud import WordCloud

from utils.ai_provider import get_ai_feedback
from utils.analysis import calculate_wpm, count_fillers, top_words, total_words
from utils.scoring import confidence_score
from utils.scoring import generate_feedback as generate_rule_feedback
from utils.transcribe import transcribe_audio

warnings.filterwarnings("ignore", message="Couldn't find ffmpeg or avconv.*")

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
HISTORY_PATH = DATA_DIR / "history.csv"
SUPPORTED_AUDIO_TYPES = ["mp3", "wav", "m4a", "mp4"]
AI_PROVIDERS = ["Local AI (Ollama)", "OpenAI API", "Gemini API"]
OLLAMA_MODELS = ["llama3", "mistral", "gemma"]


def ensure_history_file() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    if not HISTORY_PATH.exists():
        HISTORY_PATH.write_text("score,wpm,fillers\n", encoding="utf-8")


def save_history(score: int, wpm: float, fillers: int) -> None:
    ensure_history_file()
    row = pd.DataFrame([{"score": score, "wpm": wpm, "fillers": fillers}])
    row.to_csv(HISTORY_PATH, mode="a", header=False, index=False)


def audio_duration_minutes(audio_path: Path) -> float:
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    command = [ffmpeg_path, "-hide_banner", "-i", str(audio_path)]

    try:
        result = run(command, capture_output=True, text=True, check=False)
        output = f"{result.stderr}\n{result.stdout}"
        match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", output)
        if match:
            hours, minutes, seconds = match.groups()
            total_seconds = (int(hours) * 3600) + (int(minutes) * 60) + float(seconds)
            return total_seconds / 60
    except FileNotFoundError as exc:
        raise RuntimeError(f"Bundled FFmpeg executable was not found: {ffmpeg_path}") from exc

    try:
        AudioSegment.converter = ffmpeg_path
        audio = AudioSegment.from_file(audio_path)
        return len(audio) / 60000
    except (FileNotFoundError, CalledProcessError) as exc:
        raise RuntimeError("Could not read audio duration with bundled FFmpeg.") from exc


def metric_chart(label: str, value: float, max_value: float, color: str) -> go.Figure:
    return go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": label, "font": {"size": 18}},
            gauge={
                "axis": {"range": [0, max_value]},
                "bar": {"color": color},
                "bgcolor": "#f7f9fc",
                "borderwidth": 1,
                "bordercolor": "#d9e2ec",
            },
        )
    ).update_layout(height=260, margin=dict(l=24, r=24, t=44, b=12))


def style_page() -> None:
    st.set_page_config(
        page_title="SpeakWise AI",
        page_icon="🎤",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
                max-width: 1180px;
            }
            .hero {
                padding: 1.4rem 0 0.5rem;
            }
            .hero h1 {
                font-size: 3rem;
                line-height: 1.05;
                margin-bottom: 0.2rem;
            }
            .hero p {
                color: #4a5568;
                font-size: 1.2rem;
                margin-top: 0;
            }
            div[data-testid="stMetric"] {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 1rem;
                box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_wordcloud(word_counts: dict[str, int]) -> None:
    if not word_counts:
        st.info("Not enough transcript content for a word cloud yet.")
        return

    cloud = WordCloud(
        width=900,
        height=360,
        background_color="white",
        colormap="viridis",
        max_words=80,
    ).generate_from_frequencies(word_counts)
    st.image(cloud.to_array(), use_container_width=True)


def render_ai_settings() -> tuple[str, str | None, str | None]:
    with st.sidebar:
        st.header("⚙️ AI Settings")
        provider = st.radio("AI Provider", AI_PROVIDERS, index=0)
        model = None
        api_key = None

        if provider == "Local AI (Ollama)":
            model = st.selectbox("Model", OLLAMA_MODELS, index=0)
            st.caption("Privacy-first local inference at http://localhost:11434")

        st.subheader("BYOK API Keys")
        st.text_input("OpenAI API Key", type="password", key="openai_api_key")
        st.text_input("Gemini API Key", type="password", key="gemini_api_key")

        if provider == "OpenAI API":
            api_key = st.session_state.get("openai_api_key", "")
        elif provider == "Gemini API":
            api_key = st.session_state.get("gemini_api_key", "")

        st.caption("Keys are stored only in Streamlit session state and are never saved to disk.")

    return provider, model, api_key


def selected_audio_input():
    input_source = st.radio(
        "Audio source",
        ["Upload audio", "Record with microphone"],
        horizontal=True,
    )

    if input_source == "Upload audio":
        audio_file = st.file_uploader(
            "Choose an MP3, WAV, M4A, or MP4 file",
            type=SUPPORTED_AUDIO_TYPES,
            accept_multiple_files=False,
        )
        suffix = Path(audio_file.name).suffix if audio_file is not None else ".wav"
        return audio_file, suffix

    recorded_audio = st.audio_input("Record your speech")
    return recorded_audio, ".wav"


def main() -> None:
    style_page()
    ensure_history_file()
    provider, selected_model, api_key = render_ai_settings()

    st.markdown(
        """
        <div class="hero">
            <h1>🎤 SpeakWise AI</h1>
            <p>Your Personal Public Speaking Coach</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    upload_col, details_col = st.columns([1.05, 0.95], gap="large")

    with upload_col:
        st.subheader("Add Speech Recording")
        audio_file, suffix = selected_audio_input()

        if audio_file is None:
            st.info("Upload or record a speech sample to generate a transcript and coaching dashboard.")
            return

        if suffix.lower() == ".mp4":
            st.video(audio_file)
        else:
            st.audio(audio_file, format=getattr(audio_file, "type", "audio/wav"))
        analyze = st.button("Analyze Speech", type="primary", use_container_width=True)

    with details_col:
        st.subheader("What SpeakWise Measures")
        st.write("SpeakWise AI evaluates pace, filler words, vocabulary patterns, and AI-powered coaching feedback.")
        st.metric("Selected AI Provider", provider)
        if selected_model:
            st.metric("Local Model", selected_model)
        st.progress(0, text="Waiting for an audio file")

    if not analyze:
        return

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
            temp_audio.write(audio_file.getbuffer())
            audio_path = Path(temp_audio.name)

        progress = st.progress(10, text="Validating audio")
        duration_minutes = audio_duration_minutes(audio_path)
        if duration_minutes <= 0:
            st.error("The uploaded audio appears to be empty.")
            return

        progress.progress(35, text="Transcribing with Whisper")
        transcript = transcribe_audio(audio_path)
        if not transcript:
            st.error("Whisper returned an empty transcript. Try a clearer or longer recording.")
            return

        progress.progress(70, text="Analyzing delivery")
        words = total_words(transcript)
        fillers = count_fillers(transcript)
        wpm = calculate_wpm(transcript, duration_minutes)
        score = confidence_score(wpm, fillers)
        feedback = generate_rule_feedback(wpm, fillers)
        common_words = top_words(transcript)

        progress.progress(82, text="Generating AI coaching feedback")
        ai_feedback = None
        try:
            ai_feedback = get_ai_feedback(
                transcript=transcript,
                provider=provider,
                api_key=api_key,
                model=selected_model,
            )
        except ValueError as exc:
            st.warning(str(exc))
        except RuntimeError as exc:
            st.warning(str(exc))
        except Exception as exc:
            st.warning(f"AI feedback could not be generated: {exc}")

        progress.progress(92, text="Saving progress")
        save_history(score, wpm, fillers)
        progress.progress(100, text="Analysis complete")

    except Exception as exc:
        st.error(f"Could not analyze this audio file: {exc}")
        return
    finally:
        if "audio_path" in locals() and audio_path.exists():
            audio_path.unlink(missing_ok=True)

    st.divider()

    metric_col_1, metric_col_2, metric_col_3, metric_col_4 = st.columns(4)
    metric_col_1.metric("Confidence Score", f"{score}/100")
    metric_col_2.metric("Speaking Speed", f"{wpm} WPM")
    metric_col_3.metric("Filler Words", fillers)
    metric_col_4.metric("Total Words", words)

    st.subheader("Transcript")
    st.text_area("Transcript", transcript, height=220, label_visibility="collapsed")

    st.subheader("Rule-Based Feedback")
    for item in feedback:
        st.success(item)

    st.subheader("AI-Powered Coaching Analysis")
    if ai_feedback:
        st.markdown(ai_feedback)
    elif provider in ["OpenAI API", "Gemini API"] and not api_key:
        st.info("Please enter your API key.")
    elif provider == "Local AI (Ollama)":
        st.info("Local AI server not running. Start Ollama and try again.")
    else:
        st.info("AI coaching feedback is unavailable for this session.")

    st.subheader("Visual Dashboard")
    chart_col_1, chart_col_2, chart_col_3 = st.columns(3)
    chart_col_1.plotly_chart(metric_chart("Confidence Score", score, 100, "#2563eb"), use_container_width=True)
    chart_col_2.plotly_chart(metric_chart("WPM", wpm, 240, "#059669"), use_container_width=True)
    chart_col_3.plotly_chart(metric_chart("Filler Count", fillers, 40, "#dc2626"), use_container_width=True)

    st.subheader("Top Words")
    render_wordcloud(common_words)


if __name__ == "__main__":
    main()
