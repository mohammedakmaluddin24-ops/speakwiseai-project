# SpeakWiseAI User Manual

## Overview

SpeakWiseAI is a public speaking coach application that analyzes speech recordings and provides feedback on pace, filler words, confidence, and more. It supports local and API-based AI providers for generated feedback.

## Installation

1. Create a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the application

Start the app from the project root:

```bash
streamlit run app.py
```

Then open the Streamlit URL shown in the terminal.

## Using the app

1. Choose an AI provider in the sidebar.
2. Upload an audio file or record from the microphone.
3. Wait for the analysis to complete.
4. Review the score, speaking metrics, word cloud, and AI feedback.

## AI provider settings

- `Local AI (Ollama)` requires a locally hosted Ollama server.
- `OpenAI API` and `Gemini API` require valid API keys stored in session state.

## Supported input formats

- `mp3`
- `wav`
- `m4a`
- `mp4`

## Troubleshooting

- If audio upload fails, verify the file format and size.
- If API feedback does not appear, confirm your API key is correct.
- If local AI is selected, ensure Ollama is running on `http://localhost:11434`.

## File structure

- `app.py`: main Streamlit application.
- `utils/`: helper modules for AI provider, transcription, scoring, and analysis.
- `data/history.csv`: saved history for performance tracking.

## Notes

This application stores API keys only in session state and does not write them to disk.