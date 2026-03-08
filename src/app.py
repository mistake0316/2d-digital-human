import gradio as gr
import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from master_ui import demo
from model import (
    DigitalHumanRequest,
    AudioRequest,
    VideoRequest,
    TTSRequest,
)
from client.qwen3_tts import tts as _tts
from client.liveportrait import drive_by_video as _drive_by_video
from client.talking_head import talking_head as _talking_head
from config import settings

app = FastAPI()

gr.mount_gradio_app(app, demo, path="/gradio")


@app.middleware("http")
async def catch_all_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"success": False, "message": str(e)}
        )


@app.get("/")
def root(request: Request):
    return {
        "swagger-ui": f"{request.base_url}doc",
        "gradio-ui": f"{request.base_url}gradio",
    }


@app.post("/health")
def health():
    return {"status": "ok"}


@app.post("/tts")
def tts(item: TTSRequest):
    audio = _tts(item.text, item.voice_description)
    return FileResponse(audio, media_type="audio/wav", filename="output.wav")


@app.post("/video_driven")
def video_driven(item: VideoRequest):
    video = _drive_by_video(item.image_path, item.video_path)
    return FileResponse(video, media_type="video/mp4", filename="output.mp4")


@app.post("/talking_head")
def talking_head(item: AudioRequest):
    video = _talking_head(item.image_path, item.audio_path)
    return FileResponse(video, media_type="video/mp4", filename="output.mp4")


@app.post("/digital_human")
def digital_human(item: DigitalHumanRequest):
    assert not all(
        [item.background_video, item.background_image]
    ), "Only one of background_video or background_image should be provided"

    result_video = None

    # if item.face_swap_target:
    #     avatar = _faceswap(item.avatar, item.face_swap_target)

    if item.mode == "video":
        result_video = _drive_by_video(item.avatar, item.driving_video)
    elif item.mode == "audio":
        result_video = _talking_head(item.avatar, item.audio)
    elif item.mode == "tts":
        generated_audio = _tts(item.text, item.voice_description)
        result_video = _talking_head(item.avatar, generated_audio)
    elif item.mode == "motion":
        ...
        # For motion mode, we can use a default driving video or motion data.
        # Here we just reuse the driving video for simplicity.
        # reference_video = assest_pool[item.motion]
        # result_video = _drive_by_video(item.avatar, item.driving_video)
    else:
        raise ValueError("Invalid mode")

    # if item.background_video:
    #     result_video = remove_forground_add_background_video(result_video, item.background_video)
    # elif item.background_image:
    #     result_video = remove_forground_add_background_image(result_video, item.background_image)

    return FileResponse(result_video, media_type="video/mp4", filename="output.mp4")


@app.post("/return_sample_video")
def test_return_video(item: DigitalHumanRequest):
    video_path = os.path.join(settings.ASSETS_ROOT, "d0.mp4")
    return FileResponse(video_path, media_type="video/mp4", filename="output.mp4")
