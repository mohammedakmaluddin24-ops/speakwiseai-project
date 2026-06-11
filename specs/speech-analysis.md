# Speech Analysis

## Summary

SpeakWiseAI accepts an uploaded or recorded audio sample, transcribes it with Whisper, calculates speaking metrics, and presents coaching feedback in a Streamlit dashboard.

## Acceptance Criteria

- The app accepts MP3, WAV, M4A, and MP4 inputs.
- Empty or unreadable audio produces a clear error.
- The app reports confidence score, WPM, filler count, total words, transcript, rule-based feedback, optional AI feedback, and visual summaries.
- API keys are provided by the user at runtime and are not saved to repository files or local history.

## Quality Requirements

- Unit tests cover scoring and transcript analysis helpers.
- CI runs linting, type checking, security scanning, dependency audit, and coverage reporting.
