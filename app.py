import os
import tempfile
import gradio as gr
from config import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE, OUTPUT_DIR
from model import clone_voice

os.makedirs(OUTPUT_DIR, exist_ok=True)


def run_clone(ref_audio, ref_text, text_to_speak, language):
    """Gradio handler — validates inputs and runs voice cloning."""

    if ref_audio is None:
        return None, "❌ Please upload a reference audio file."

    if not ref_text.strip():
        return None, "❌ Please provide the transcript of your reference audio."

    if not text_to_speak.strip():
        return None, "❌ Please enter the text you want the cloned voice to say."

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".wav", dir=OUTPUT_DIR, delete=False
        ) as f:
            output_path = f.name

        clone_voice(
            text=text_to_speak,
            ref_audio=ref_audio,
            ref_text=ref_text,
            language=language,
            output_path=output_path,
        )
        return output_path, "✅ Done! Play the audio below."

    except Exception as e:
        return None, f"❌ Error: {str(e)}"


with gr.Blocks(title="MimicTTS") as demo:
    gr.Markdown("# MimicTTS\nVoice cloning powered by Qwen3-TTS.")

    with gr.Row():
        with gr.Column():
            ref_audio = gr.Audio(type="filepath", label="Reference Voice (3–15 sec)")
            ref_text = gr.Textbox(
                label="Reference Transcript",
                placeholder="Exact words spoken in the reference audio...",
            )
            text_input = gr.Textbox(
                label="Text to Speak",
                placeholder="What should the cloned voice say?",
                lines=3,
            )
            language = gr.Dropdown(
                SUPPORTED_LANGUAGES, value=DEFAULT_LANGUAGE, label="Language"
            )
            submit_btn = gr.Button("🎤 Clone Voice", variant="primary")

        with gr.Column():
            output_audio = gr.Audio(label="Cloned Output", type="filepath")
            status_msg = gr.Textbox(label="Status", interactive=False)

    submit_btn.click(
        fn=run_clone,
        inputs=[ref_audio, ref_text, text_input, language],
        outputs=[output_audio, status_msg],
    )

if __name__ == "__main__":
    from config import GRADIO_SHARE, GRADIO_PORT

    demo.launch(share=GRADIO_SHARE, server_port=GRADIO_PORT)
