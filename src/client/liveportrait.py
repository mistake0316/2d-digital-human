import gradio as gr
from gradio_client import Client, handle_file
from config import settings


def drive_by_video(image: str, video: str) -> str:
    client = Client(
        settings.HF_SPACE_LIVEPORTRAIT,
        token=settings.HF_TOKEN_LIVEPORTRAIT,
        verbose=False,
    )
    result = client.predict(
        param_0=handle_file(image),
        param_1={"video": handle_file(video)},
        api_name="/gpu_wrapped_execute_video",
    )
    animated_video = result[0]["video"]
    return animated_video


demo = gr.Interface(
    fn=drive_by_video,
    inputs=[
        gr.Image(type="filepath", label="Input Image"),
        gr.Video(label="Driving Video"),
    ],
    outputs=gr.Video(),
    api_name="liveportrait",
)
