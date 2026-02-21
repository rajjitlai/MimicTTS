import json
import os

from config import (
    DEFAULT_LANGUAGE,
    DEFAULT_OUTPUT_FILE,
    OUTPUT_DIR,
    REFERENCE_AUDIO_DIR,
    SUPPORTED_LANGUAGES,
)
from model import clone_voice

TRANSCRIPT_STORE = os.path.join(REFERENCE_AUDIO_DIR, "transcripts.json")


# ── Transcript Store ───────────────────────────────────────────────────────────


def _load_transcripts() -> dict:
    """Load the saved transcript map from disk."""
    if os.path.isfile(TRANSCRIPT_STORE):
        with open(TRANSCRIPT_STORE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_transcript(filename: str, transcript: str) -> None:
    """Persist a transcript for a given audio filename."""
    store = _load_transcripts()
    store[filename] = transcript
    with open(TRANSCRIPT_STORE, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)


# ── UI Helpers ─────────────────────────────────────────────────────────────────


def print_banner() -> None:
    print("")
    print("╔══════════════════════════════════════════╗")
    print("║              MimicTTS                   ║")
    print("║       Interactive Voice Cloner           ║")
    print("╚══════════════════════════════════════════╝")
    print("")


def pick_reference_audio() -> str:
    """List .wav/.mp3 files in reference_audio/ and let user pick one."""
    supported = (".wav", ".mp3")
    files = [f for f in os.listdir(REFERENCE_AUDIO_DIR) if f.endswith(supported)]

    if not files:
        print(f"No audio files found in '{REFERENCE_AUDIO_DIR}/'.")
        print("   Drop a .wav or .mp3 file there and re-run.\n")
        exit(1)

    store = _load_transcripts()
    print("Reference audio files available:")
    for i, f in enumerate(files, 1):
        tag = "  [transcript saved]" if f in store else ""
        print(f"   [{i}] {f}{tag}")
    print("")

    while True:
        choice = input("Pick a file by number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            selected_name = files[int(choice) - 1]
            selected_path = os.path.join(REFERENCE_AUDIO_DIR, selected_name)
            print(f"   Using: {selected_path}\n")
            return selected_path
        print("   Invalid choice, try again.")


def get_ref_text(audio_path: str) -> str:
    """
    Return the reference transcript for the given audio file.

    If a transcript is already saved, show it and let the user confirm,
    edit, or replace it. Otherwise prompt for input and save it.
    """
    filename = os.path.basename(audio_path)
    store = _load_transcripts()

    if filename in store:
        saved = store[filename]
        print("Reference transcript (saved):")
        print(f"   {saved}")
        print("")
        print("   [Enter] Use this   [e] Edit   [n] Replace with new")
        choice = input("Choice: ").strip().lower()
        print("")

        if choice == "" or choice == "y":
            return saved

        if choice == "e":
            print("Edit the transcript (press Enter when done):")
            edited = input("> ").strip()
            if edited:
                _save_transcript(filename, edited)
                return edited
            print("   No input — keeping saved transcript.\n")
            return saved

        # 'n' — fall through to prompt new transcript below

    print("Reference transcript")
    print("   (Type out exactly what is spoken in your reference audio)")
    while True:
        text = input("Transcript: ").strip()
        if text:
            _save_transcript(filename, text)
            print("   Transcript saved for next time.\n")
            return text
        print("   Transcript cannot be empty.")


def ask_text_to_speak() -> str:
    print("Text to speak")
    print("   (What should the cloned voice say?)")
    while True:
        text = input("Text: ").strip()
        if text:
            print("")
            return text
        print("   Text cannot be empty.")


def pick_language() -> str:
    print("Language selection:")
    for i, lang in enumerate(SUPPORTED_LANGUAGES, 1):
        marker = " <- default" if lang == DEFAULT_LANGUAGE else ""
        print(f"   [{i}] {lang}{marker}")
    print("")

    while True:
        choice = input(
            f"Pick a language (or press Enter for {DEFAULT_LANGUAGE}): "
        ).strip()

        if choice == "":
            print(f"   Using default: {DEFAULT_LANGUAGE}\n")
            return DEFAULT_LANGUAGE

        if choice.isdigit() and 1 <= int(choice) <= len(SUPPORTED_LANGUAGES):
            selected = SUPPORTED_LANGUAGES[int(choice) - 1]
            print(f"   Selected: {selected}\n")
            return selected

        print("   Invalid choice, try again.")


def confirm(ref_audio, ref_text, text_to_speak, language, output_path) -> bool:
    print("─" * 46)
    print("  Review your inputs before generating:")
    print("─" * 46)
    print(f"  Reference audio : {ref_audio}")
    print(f"  Transcript      : {ref_text}")
    print(f"  Text to speak   : {text_to_speak}")
    print(f"  Language        : {language}")
    print(f"  Output file     : {output_path}")
    print("─" * 46)
    print("")

    answer = input("Looks good? Generate now? [Y/n]: ").strip().lower()
    return answer in ("", "y", "yes")


def main() -> None:
    print_banner()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    ref_audio = pick_reference_audio()
    ref_text = get_ref_text(ref_audio)
    text_to_speak = ask_text_to_speak()
    language = pick_language()
    output_path = DEFAULT_OUTPUT_FILE

    if not confirm(ref_audio, ref_text, text_to_speak, language, output_path):
        print("\nCancelled. Re-run when you're ready.\n")
        return

    print("\nGenerating cloned audio...\n")
    clone_voice(
        text=text_to_speak,
        ref_audio=ref_audio,
        ref_text=ref_text,
        language=language,
        output_path=output_path,
    )

    print("")
    print("╔══════════════════════════════════════════╗")
    print("║  Done! Your audio is ready.             ║")
    print(f"║  Saved to: {output_path:<31}║")
    print("╚══════════════════════════════════════════╝")
    print("")


if __name__ == "__main__":
    main()
