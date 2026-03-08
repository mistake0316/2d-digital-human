import gradio as gr
from gradio_client import Client
from config import settings


def tts(text: str, voice_description: str) -> str:
    client = Client(
        settings.HF_SPACE_QWEN3_TTS, token=settings.HF_TOKEN_QWEN3_TTS, verbose=False
    )
    result = client.predict(
        text=text,
        language="Auto",
        voice_description=voice_description,
        api_name="/generate_voice_design",
    )
    return result[0]


demo = gr.Interface(
    fn=tts,
    inputs=["text", "text"],
    outputs=gr.Audio(),
    api_name="qwen3-tts",
)
