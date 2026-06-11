# SpeakWiseAI Constitution

## Principles

1. User audio and transcripts are private by default. API keys stay in session state and are never written to disk.
2. Speech analysis must explain measurable signals such as pace, filler words, transcript length, and coaching feedback.
3. Changes must include tests or a clear reason tests are not practical.
4. Quality gates include linting, type checks, security scanning, dependency audit, and coverage reporting.
5. Features begin with a short specification before implementation when behavior affects users.

## Governance

Specs in `specs/` describe intended behavior. Pull requests should reference the relevant spec or update it when product behavior changes.
