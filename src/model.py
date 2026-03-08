from typing import Literal
from pydantic import BaseModel


class AudioRequest(BaseModel):
    image_path: str
    audio_path: str


class VideoRequest(BaseModel):
    image_path: str
    video_path: str


class TTSRequest(BaseModel):
    text: str
    voice_description: str


class ListAvatarRequest(BaseModel): ...


class AvatarInfo(BaseModel):
    name: str
    gender: str
    description: str


class ListAvatarResponse(BaseModel):
    avatars: list[AvatarInfo]


class ListVoiceNamesRequest(BaseModel): ...


class VoiceInfo(BaseModel):
    name: str
    description: str


class ListVoiceNamesResponse(BaseModel):
    voices: list[VoiceInfo]


class DigitalHumanRequest(BaseModel):
    avatar: str
    mode: Literal["tts", "audio", "video", "motion"]

    face_swap_target: str | None = None
    # tts
    text: str | None = None
    voice_description: str | None = None
    voice_name: str | None = None

    # audio
    audio: str | None = None

    # video driven
    driving_video: str | None = None

    # motion
    motion: str | None = None  # blinking, head movement, shake head, lip open, etc.

    # replace background
    background_video: str | None = None
    background_image: str | None = None
