from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

APP_DIR = Path(__file__).resolve().parents[1]
HISTORY_PATH = APP_DIR / "data" / "history.csv"


def load_history() -> pd.DataFrame:
    if not HISTORY_PATH.exists():
        return pd.DataFrame(columns=["score", "wpm", "fillers"])

    try:
        history = pd.read_csv(HISTORY_PATH)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=["score", "wpm", "fillers"])

    expected_columns = ["score", "wpm", "fillers"]
    for column in expected_columns:
        if column not in history.columns:
            history[column] = pd.Series(dtype="float")

    return history[expected_columns].dropna(how="all")


def main() -> None:
    st.set_page_config(page_title="Progress | SpeakWise AI", page_icon="📈", layout="wide")

    st.title("📈 Progress")
    st.caption("Track how your speaking confidence improves across sessions.")

    history = load_history()
    if history.empty:
        st.info("No saved sessions yet. Analyze a speech recording from the home page to start tracking progress.")
        return

    history = history.reset_index(drop=True)
    history.index = history.index + 1
    history["session"] = history.index

    metric_col_1, metric_col_2, metric_col_3 = st.columns(3)
    metric_col_1.metric("Average Score", f"{history['score'].mean():.1f}/100")
    metric_col_2.metric("Best Score", f"{history['score'].max():.0f}/100")
    metric_col_3.metric("Sessions", len(history))

    st.subheader("Historical Table")
    st.dataframe(
        history[["score", "wpm", "fillers"]],
        use_container_width=True,
        hide_index=False,
    )

    st.subheader("Score Trend")
    trend = px.line(
        history,
        x="session",
        y="score",
        markers=True,
        labels={"session": "Session", "score": "Confidence Score"},
        range_y=[0, 100],
    )
    trend.update_traces(line_color="#2563eb", marker_size=9)
    trend.update_layout(height=420, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(trend, use_container_width=True)


if __name__ == "__main__":
    main()
