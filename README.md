# MimicTTS

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)
![Model](https://img.shields.io/badge/Model-Qwen3--TTS-purple?style=flat-square&logo=huggingface&logoColor=white)
![License](https://img.shields.io/badge/License-Research%20%2F%20Personal-orange?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=flat-square)
![CUDA](https://img.shields.io/badge/CUDA-Optional-green?style=flat-square&logo=nvidia&logoColor=white)

**Voice cloning from a short audio clip. Powered by [Qwen3-TTS](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base) — an open-source model by Alibaba.**

Clone any voice from a 3 to 15 second reference audio clip and generate new speech in that voice. Run it interactively, via CLI flags, or through a browser-based UI.

</div>

---

## Features

| Category | Details |
|---|---|
| Voice Cloning | Clone any voice from a 3 to 15 second clean reference clip |
| Languages | English, Chinese, Japanese, Korean, German, French, Russian, Spanish, Italian, Portuguese |
| Interfaces | Interactive runner, CLI script, and Gradio web UI |
| Models | Lightweight 0.6B and higher quality 1.7B model options |
| Configuration | Fully configurable via `.env` — no code changes needed |
| Hardware | Runs on CUDA GPU (4 to 8GB VRAM) or CPU |

---

## Requirements

- Python 3.10 or higher
- CUDA GPU with 4 to 8GB VRAM (or CPU for slower testing)
- A reference audio clip: `.wav` or `.mp3`, 3 to 15 seconds, clean speech, no background noise

---

## Setup

**1. Clone the repository**

```bash
git clone https://github.com/rajjitlai/MimicTTS.git
cd MimicTTS
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. (Optional) Install Flash Attention for faster GPU inference**

```bash
pip install flash-attn --no-build-isolation
```

**5. Configure your environment**

```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

Open `.env` and fill in your values. At minimum, set `HF_TOKEN` — a **read-access** token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) — to allow model downloads.

**6. (Optional) Log in to HuggingFace CLI**

```bash
huggingface-cli login
```

---

## Usage

### Interactive Runner (Recommended)

Drop your reference audio into `reference_audio/`, then run:

```bash
python runner.py
```

The runner guides you through every step with clear prompts:

```
+------------------------------------------+
|              MimicTTS                    |
|       Interactive Voice Cloner           |
+------------------------------------------+

Reference audio files available:
   [1] my_voice.wav
   [2] sample.wav

Pick a file by number: 1
   Using: reference_audio/my_voice.wav

Reference transcript
   (Type out exactly what is spoken in your reference audio)
Transcript: Hello, my name is John and this is my voice.

Text to speak
   (What should the cloned voice say?)
Text: Welcome to my project, thanks for watching!

Language selection:
   [1] English  <- default
   [2] Chinese
   ...

Pick a language (or press Enter for English):
   Using default: English

------------------------------------------
  Review your inputs before generating:
------------------------------------------
  Reference audio : reference_audio/my_voice.wav
  Transcript      : Hello, my name is John and this is my voice.
  Text to speak   : Welcome to my project, thanks for watching!
  Language        : English
  Output file     : outputs/result.wav
------------------------------------------

Looks good? Generate now? [Y/n]:
```

Output is saved to `outputs/result.wav` (configurable in `.env`).

---

### CLI

For power users who prefer flags:

```bash
python voice_clone.py \
  --ref_audio reference_audio/my_voice.wav \
  --ref_text "This is what is spoken in the reference audio." \
  --text "Hello, this is my cloned voice speaking something new!" \
  --language English \
  --output outputs/result.wav
```

**Arguments:**

| Argument | Required | Default | Description |
|---|---|---|---|
| `--ref_audio` | Yes | — | Path to reference audio (.wav or .mp3) |
| `--ref_text` | Yes | — | Exact transcript of the reference audio |
| `--text` | Yes | — | New text for the cloned voice to speak |
| `--language` | No | English | Output language |
| `--output` | No | `outputs/result.wav` | Output file path |

---

### Web UI

```bash
python app.py
```

Open `http://localhost:7860` in your browser. Upload your reference audio, fill in the transcript, type what you want the cloned voice to say, and click **Clone Voice**.

To expose the UI on your local network (for example, running on a remote machine or WSL), set `GRADIO_SHARE=true` in your `.env`.

---

## Project Structure

```
MimicTTS/
├── runner.py               # Interactive step-by-step prompt (recommended entry point)
├── app.py                  # Gradio web UI
├── voice_clone.py          # CLI script with argument flags
├── model.py                # Model loading and inference (shared singleton)
├── config.py               # Central config — reads from .env
├── reference_audio/        # Place your reference .wav/.mp3 files here
├── outputs/                # Generated audio files are saved here
├── requirements.txt        # Python dependencies
├── .env                    # Your local config (not committed to git)
├── .env.example            # Config template — copy to .env to get started
├── .gitignore
└── README.md
```

---

## Configuration

All settings are controlled via your `.env` file. Copy `.env.example` to `.env` to get started.

| Variable | Default | Description |
|---|---|---|
| `MODEL_ID` | `Qwen/Qwen3-TTS-12Hz-0.6B-Base` | HuggingFace model to use |
| `DEVICE` | Auto-detected | `cuda:0`, `cuda:1`, or `cpu` |
| `REFERENCE_AUDIO_DIR` | `reference_audio` | Folder for input audio files |
| `OUTPUT_DIR` | `outputs` | Folder for generated audio files |
| `DEFAULT_LANGUAGE` | `English` | Fallback language |
| `DEFAULT_OUTPUT_FILE` | `outputs/result.wav` | Where `runner.py` saves output |
| `GRADIO_SHARE` | `false` | Set `true` to expose UI on your network |
| `GRADIO_PORT` | `7860` | Port for the Gradio web UI |
| `HF_TOKEN` | — | HuggingFace read token for model downloads |

---

## Model Options

| Model | Size | VRAM | Best For |
|---|---|---|---|
| `Qwen3-TTS-12Hz-0.6B-Base` | 2.5 GB | ~4 GB | Quick tests, lighter hardware |
| `Qwen3-TTS-12Hz-1.7B-Base` | 4.5 GB | 6 to 8 GB | Better quality, production use |

Switch models by changing `MODEL_ID` in your `.env` file.

---

## Tips for Best Results

- **Reference audio quality is the single biggest factor.** Record in a quiet room with no background noise.
- A **5 to 10 second clip** is the sweet spot. Too short loses voice character; too long adds no benefit.
- **Always provide the reference transcript.** Skipping it noticeably degrades clone quality.
- **Match the language to the language you are generating**, not the language of the reference audio.
- If you encounter GPU out-of-memory errors, set `DEVICE=cpu` in `.env` or switch to the 0.6B model.

---

## License

This project is for personal and research use. The underlying Qwen3-TTS model is subject to its own [license on HuggingFace](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base). Please review it before any commercial use.
