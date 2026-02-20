# Simple_TTS_CLI

A simple voice cloning tool powered by [Qwen3-TTS](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base) — an open-source TTS model by Alibaba. Clone any voice from a 3–15 second reference audio clip and generate new speech in that voice, via an interactive prompt, CLI, or a browser-based UI.

---

## Features

- Voice cloning from a short reference audio clip (3–15 seconds)
- Supports 10 languages: English, Chinese, Japanese, Korean, German, French, Russian, Spanish, Italian, Portuguese
- Interactive step-by-step runner — no command flags needed
- CLI script for power users
- Gradio web UI for a browser-based experience
- Lightweight 0.6B and higher quality 1.7B model options
- Fully configurable via `.env` file

---

## Requirements

- Python 3.10+
- CUDA GPU with 4–8GB VRAM (or CPU for slower testing)
- A short `.wav` or `.mp3` reference audio clip (3–15 seconds, clean speech, no background noise)

---

## Setup

**1. Clone the repository**

```bash
git clone https://github.com/your-username/Simple_TTS_CLI.git
cd Simple_TTS_CLI
```

**2. Create and activate a virtual environment**

```bash
python -m venv qwen-tts-env

# Windows
qwen-tts-env\Scripts\activate

# Linux / macOS
source qwen-tts-env/bin/activate
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

Open `.env` and fill in your values. At minimum, set your `HF_TOKEN` (a **read-access** token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)) to allow model downloads.

**6. (Optional) Log in to HuggingFace CLI**

```bash
huggingface-cli login
```

---

## Usage

### ✅ Interactive Runner (recommended)

Drop your reference audio into `reference_audio/`, then just run:

```bash
python runner.py
```

The runner will guide you through every step:

```
╔══════════════════════════════════════════╗
║          Simple_TTS_CLI  🎙️              ║
║       Interactive Voice Cloner           ║
╚══════════════════════════════════════════╝

📂 Reference audio files available:
   [1] my_voice.wav
   [2] sample.wav

👉 Pick a file by number: 1
   ✅ Using: reference_audio/my_voice.wav

📝 Reference transcript
   (Type out exactly what is spoken in your reference audio)
👉 Transcript: Hello, my name is John and this is my voice.

💬 Text to speak
   (What should the cloned voice say?)
👉 Text: Welcome to my project, thanks for watching!

🌐 Language selection:
   [1] English ◀ default
   [2] Chinese
   ...

👉 Pick a language (or press Enter for English):
   ✅ Using default: English

──────────────────────────────────────────────
  Review your inputs before generating:
──────────────────────────────────────────────
  Reference audio : reference_audio/my_voice.wav
  Transcript      : Hello, my name is John and this is my voice.
  Text to speak   : Welcome to my project, thanks for watching!
  Language        : English
  Output file     : outputs/result.wav
──────────────────────────────────────────────

👉 Looks good? Generate now? [Y/n]:
```

The output is saved automatically to `outputs/result.wav` (configurable in `.env`).

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

All arguments:

| Argument      | Required | Default            | Description                             |
| ------------- | -------- | ------------------ | --------------------------------------- |
| `--ref_audio` | ✅       | —                  | Path to reference audio (.wav or .mp3)  |
| `--ref_text`  | ✅       | —                  | Exact transcript of the reference audio |
| `--text`      | ✅       | —                  | New text for the cloned voice to speak  |
| `--language`  | ❌       | English            | Output language                         |
| `--output`    | ❌       | outputs/result.wav | Output file path                        |

---

### Web UI

```bash
python app.py
```

Then open `http://localhost:7860` in your browser. Upload your reference audio, fill in the transcript, type what you want the cloned voice to say, and hit **Clone Voice**.

To expose the UI on your local network (e.g. running on a remote machine or WSL), set `GRADIO_SHARE=true` in your `.env`.

---

## Project Structure

```
Simple_TTS_CLI/
├── runner.py               # ✅ Interactive step-by-step prompt (start here)
├── app.py                  # Gradio web UI
├── voice_clone.py          # CLI script
├── model.py                # Model loading & inference (shared)
├── config.py               # Central config — reads from .env
├── reference_audio/        # Place your reference .wav/.mp3 files here
├── outputs/                # Generated audio files saved here
├── requirements.txt        # Python dependencies
├── .env                    # Your local config (never committed)
├── .env.example            # Config template — copy to .env to get started
├── .gitignore
└── README.md
```

---

## Configuration

All settings are controlled via your `.env` file. Copy `.env.example` to `.env` to get started.

| Variable              | Default                    | Description                                    |
| --------------------- | -------------------------- | ---------------------------------------------- |
| `MODEL_ID`            | `Qwen3-TTS-12Hz-0.6B-Base` | HuggingFace model to use                       |
| `DEVICE`              | auto-detected              | `cuda:0`, `cuda:1`, or `cpu`                   |
| `REFERENCE_AUDIO_DIR` | `reference_audio`          | Folder for input audio files                   |
| `OUTPUT_DIR`          | `outputs`                  | Folder for generated audio files               |
| `DEFAULT_LANGUAGE`    | `English`                  | Fallback language                              |
| `DEFAULT_OUTPUT_FILE` | `outputs/result.wav`       | Where runner.py saves output                   |
| `GRADIO_SHARE`        | `false`                    | Set `true` to expose UI on your network        |
| `GRADIO_PORT`         | `7860`                     | Port for the Gradio web UI                     |
| `HF_TOKEN`            | —                          | HuggingFace **read** token for model downloads |

---

## Model Options

| Model                      | Size  | VRAM   | Best For                       |
| -------------------------- | ----- | ------ | ------------------------------ |
| `Qwen3-TTS-12Hz-0.6B-Base` | 2.5GB | ~4GB   | Quick tests, lighter hardware  |
| `Qwen3-TTS-12Hz-1.7B-Base` | 4.5GB | ~6–8GB | Better quality, production use |

Switch models by changing `MODEL_ID` in your `.env` file.

---

## Tips for Best Results

- Reference audio quality is the single biggest factor — record in a quiet room with no background noise
- A 5–10 second clip is the sweet spot; too short loses voice character, too long adds no benefit
- Always provide the reference transcript — skipping it noticeably degrades clone quality
- Match the language to the language you're generating, not the reference audio
- If you run into GPU out-of-memory errors, set `DEVICE=cpu` in `.env` or switch to the 0.6B model

---

## License

This project is for personal and research use. The underlying Qwen3-TTS model is subject to its own [license on HuggingFace](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base). Please review it before any commercial use.
