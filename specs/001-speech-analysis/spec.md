# Feature Specification: Speech Analysis

## User Scenarios

- As a speaker, I want to upload or record a speech sample so that I can review a transcript and delivery metrics.
- As a learner, I want coaching feedback so that I can improve pace, clarity, and filler-word control.

## Requirements

- The app accepts MP3, WAV, M4A, and MP4 inputs.
- Empty or unreadable audio produces a clear error.
- Results include confidence score, WPM, filler count, total words, transcript, feedback, and charts.
- API keys are provided at runtime and are not written to disk.

## Acceptance Criteria

- [ ] Unit tests cover scoring and transcript helper functions.
- [ ] CI runs lint, format, type-check, security, dependency-audit, and coverage jobs.
