import gradio as gr
from gradio_client import Client, handle_file
from config import settings


def talking_head(image: str, audio: str) -> str:
    client = Client(
        settings.HF_SPACE_TALKING_HEAD,
        token=settings.HF_TOKEN_TALKING_HEAD,
        verbose=False,
    )
    result = client.predict(
        uploaded_img=handle_file(image),
        uploaded_audio=handle_file(audio),
        api_name="/generate_video",
    )
    animated_video = result["video"]
    return animated_video


demo = gr.Interface(
    fn=talking_head,
    inputs=[
        gr.Image(type="filepath", label="Input Image"),
        gr.Audio(label="Input Audio", type="filepath"),
    ],
    outputs=gr.Video(),
    api_name="echomimic",
)
