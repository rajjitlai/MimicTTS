import torch
import os
from dotenv import load_dotenv

load_dotenv()

# ── Model ─────────────────────────────────────────────────────────────────────
MODEL_ID = os.getenv("MODEL_ID", "Qwen/Qwen3-TTS-12Hz-0.6B-Base")

# ── Device ────────────────────────────────────────────────────────────────────
_device_env = os.getenv("DEVICE", "").strip()

if _device_env:
    DEVICE = _device_env
else:
    DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"

DTYPE = torch.bfloat16 if "cuda" in DEVICE else torch.float32
USE_FLASH_ATTN = "cuda" in DEVICE

# ── Paths ─────────────────────────────────────────────────────────────────────
REFERENCE_AUDIO_DIR = os.getenv("REFERENCE_AUDIO_DIR", "reference_audio")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "outputs")

# ── Defaults ──────────────────────────────────────────────────────────────────
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "English")
DEFAULT_OUTPUT_FILE = os.getenv("DEFAULT_OUTPUT_FILE", "outputs/result.wav")

# ── Gradio ────────────────────────────────────────────────────────────────────
GRADIO_SHARE = os.getenv("GRADIO_SHARE", "false").lower() == "true"
GRADIO_PORT = int(os.getenv("GRADIO_PORT", 7860))

# ── HuggingFace ───────────────────────────────────────────────────────────────
HF_TOKEN = os.getenv("HF_TOKEN", None)

# ── Supported Languages ───────────────────────────────────────────────────────
SUPPORTED_LANGUAGES = [
    "English",
    "Chinese",
    "Japanese",
    "Korean",
    "German",
    "French",
    "Russian",
    "Spanish",
    "Italian",
    "Portuguese",
]
