import soundfile as sf
from qwen_tts import Qwen3TTSModel
from transformers import logging as hf_logging

from config import DEVICE, DTYPE, HF_TOKEN, MODEL_ID, USE_FLASH_ATTN
from progress import TTSProgressSpinner

# Suppress HuggingFace's "Setting pad_token_id to eos_token_id" warning spam
hf_logging.set_verbosity_error()

# Module-level singleton so the model is only loaded once
_model = None


def get_model() -> Qwen3TTSModel:
    """Load and cache the Qwen3-TTS model (loads once per session)."""
    global _model

    if _model is not None:
        return _model

    if not HF_TOKEN:
        print(
            "WARNING: HF_TOKEN is not set in your .env file.\n"
            "         Model downloads from HuggingFace may fail for gated models.\n"
            "         Get a read token at https://huggingface.co/settings/tokens\n"
        )

    print(f"Loading model: {MODEL_ID}")
    print(f"Device: {DEVICE} | dtype: {DTYPE}")

    kwargs = {
        "device_map": DEVICE,
        "dtype": DTYPE,
    }

    if USE_FLASH_ATTN:
        kwargs["attn_implementation"] = "flash_attention_2"

    _model = Qwen3TTSModel.from_pretrained(MODEL_ID, **kwargs)
    print("✅ Model loaded successfully.\n")
    return _model


def clone_voice(
    text: str,
    ref_audio: str,
    ref_text: str,
    language: str = "English",
    output_path: str = "outputs/result.wav",
) -> str:
    """
    Generate speech in the cloned voice and save to output_path.

    Args:
        text:        The new text you want the cloned voice to say.
        ref_audio:   Path to the reference audio file (.wav or .mp3).
        ref_text:    Transcript of the reference audio.
        language:    Output language (must match SUPPORTED_LANGUAGES in config).
        output_path: Where to save the generated .wav file.

    Returns:
        output_path on success.
    """
    model = get_model()

    print(f"Cloning voice from: {ref_audio}")
    print(f'Generating: "{text}"')
    print()

    with TTSProgressSpinner():
        wavs, sr = model.generate_voice_clone(
            text=text,
            language=language,
            ref_audio=ref_audio,
            ref_text=ref_text,
            x_vector_only_mode=True,
        )

    sf.write(output_path, wavs[0], sr)
    print(f"Saved to: {output_path}")
    return output_path
