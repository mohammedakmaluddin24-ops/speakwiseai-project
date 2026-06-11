# Agents for SpeakWiseAI

This document describes the AI agent and provider concepts used in the SpeakWiseAI project.

## What is an agent?

In SpeakWiseAI, an agent is the component responsible for generating AI-powered feedback and analysis based on speech transcripts. The agent may use different providers depending on configuration.

## Supported AI providers

- `Local AI (Ollama)` — uses a local model served via Ollama.
- `OpenAI API` — uses OpenAI's API for speech and feedback generation.
- `Gemini API` — uses Google Gemini for AI responses.

## How to configure agents

1. Choose the AI provider in the application sidebar.
2. For `Local AI (Ollama)`, select the model from the provided list.
3. For API-based providers, enter the corresponding API key in the sidebar.
4. The application stores API keys only in session state and does not write them to disk.

## Extending agent support

- Add additional provider options in `app.py` under `AI_PROVIDERS`.
- Implement the new provider logic in `utils/ai_provider.py`.
- Ensure the UI collects any required keys or configuration values.
- Test the new provider end-to-end with sample audio input.

## Notes

- Local provider support is best for privacy-first usage.
- API providers require network access and valid credentials.
- Keep provider-specific logic separate from core transcription and scoring workflows.
