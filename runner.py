import os

from config import (
    DEFAULT_LANGUAGE,
    DEFAULT_OUTPUT_FILE,
    OUTPUT_DIR,
    REFERENCE_AUDIO_DIR,
    SUPPORTED_LANGUAGES,
)
from model import clone_voice


def print_banner():
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
        print(f"❌ No audio files found in '{REFERENCE_AUDIO_DIR}/'.")
        print(f"   Drop a .wav or .mp3 file there and re-run.\n")
        exit(1)

    print("📂 Reference audio files available:")
    for i, f in enumerate(files, 1):
        print(f"   [{i}] {f}")
    print("")

    while True:
        choice = input("👉 Pick a file by number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            selected = os.path.join(REFERENCE_AUDIO_DIR, files[int(choice) - 1])
            print(f"   ✅ Using: {selected}\n")
            return selected
        print("   ⚠️  Invalid choice, try again.")


def ask_ref_text() -> str:
    print("📝 Reference transcript")
    print("   (Type out exactly what is spoken in your reference audio)")
    while True:
        text = input("👉 Transcript: ").strip()
        if text:
            print("")
            return text
        print("   ⚠️  Transcript cannot be empty.")


def ask_text_to_speak() -> str:
    print("💬 Text to speak")
    print("   (What should the cloned voice say?)")
    while True:
        text = input("👉 Text: ").strip()
        if text:
            print("")
            return text
        print("   ⚠️  Text cannot be empty.")


def pick_language() -> str:
    print("🌐 Language selection:")
    for i, lang in enumerate(SUPPORTED_LANGUAGES, 1):
        marker = " ◀ default" if lang == DEFAULT_LANGUAGE else ""
        print(f"   [{i}] {lang}{marker}")
    print("")

    while True:
        choice = input(
            f"👉 Pick a language (or press Enter for {DEFAULT_LANGUAGE}): "
        ).strip()

        if choice == "":
            print(f"   ✅ Using default: {DEFAULT_LANGUAGE}\n")
            return DEFAULT_LANGUAGE

        if choice.isdigit() and 1 <= int(choice) <= len(SUPPORTED_LANGUAGES):
            selected = SUPPORTED_LANGUAGES[int(choice) - 1]
            print(f"   ✅ Selected: {selected}\n")
            return selected

        print("   ⚠️  Invalid choice, try again.")


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

    answer = input("👉 Looks good? Generate now? [Y/n]: ").strip().lower()
    return answer in ("", "y", "yes")


def main():
    print_banner()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    ref_audio = pick_reference_audio()
    ref_text = ask_ref_text()
    text_to_speak = ask_text_to_speak()
    language = pick_language()
    output_path = DEFAULT_OUTPUT_FILE

    if not confirm(ref_audio, ref_text, text_to_speak, language, output_path):
        print("\n🚫 Cancelled. Re-run when you're ready.\n")
        return

    print("\n⏳ Generating cloned audio...\n")
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
