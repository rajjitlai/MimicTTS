# Changelog

All notable changes to MimicTTS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [1.0.0] - 2026-02-21

### Added

- Interactive step-by-step runner (`runner.py`) for guided voice cloning
- CLI script (`voice_clone.py`) with full argument flag support
- Gradio web UI (`app.py`) accessible at `localhost:7860`
- Shared model loading with singleton pattern (`model.py`)
- Central `.env`-based configuration (`config.py`)
- Support for 10 languages: English, Chinese, Japanese, Korean, German, French, Russian, Spanish, Italian, Portuguese
- Lightweight 0.6B and higher quality 1.7B Qwen3-TTS model options
- Flash Attention 2 support for faster GPU inference
- `GRADIO_SHARE` option to expose web UI on local network
- `.env.example` template for easy setup
- Full `README.md` with badges, feature table, and configuration reference

[Unreleased]: https://github.com/rajjitlai/MimicTTS/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/rajjitlai/MimicTTS/releases/tag/v1.0.0
