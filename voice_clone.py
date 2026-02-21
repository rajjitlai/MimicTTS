import argparse
import os
from config import (
    DEFAULT_LANGUAGE,
    DEFAULT_OUTPUT_FILE,
    SUPPORTED_LANGUAGES,
    OUTPUT_DIR,
)
from model import clone_voice


def parse_args():
    parser = argparse.ArgumentParser(
        description="MimicTTS — Voice Cloner using Qwen3-TTS"
    )
    parser.add_argument(
        "--ref_audio",
        type=str,
        required=True,
        help="Path to the reference audio file (3–15 sec, .wav or .mp3)",
    )
    parser.add_argument(
        "--ref_text",
        type=str,
        required=True,
        help="Exact transcript of the reference audio",
    )
    parser.add_argument(
        "--text",
        type=str,
        required=True,
        help="The new text you want the cloned voice to speak",
    )
    parser.add_argument(
        "--language",
        type=str,
        default=DEFAULT_LANGUAGE,
        choices=SUPPORTED_LANGUAGES,
        help=f"Output language (default: {DEFAULT_LANGUAGE})",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=DEFAULT_OUTPUT_FILE,
        help=f"Output .wav file path (default: {DEFAULT_OUTPUT_FILE})",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Validate reference audio exists
    if not os.path.isfile(args.ref_audio):
        print(f"❌ Reference audio not found: {args.ref_audio}")
        return

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    clone_voice(
        text=args.text,
        ref_audio=args.ref_audio,
        ref_text=args.ref_text,
        language=args.language,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()
