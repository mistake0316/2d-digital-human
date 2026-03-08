from dotenv import load_dotenv

load_dotenv()

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    HF_SPACE_LIVEPORTRAIT: str = os.getenv(
        "HF_SPACE_LIVEPORTRAIT", "KlingTeam/LivePortrait"
    )
    HF_SPACE_QWEN3_TTS: str = os.getenv("HF_SPACE_QWEN3_TTS", "Qwen/Qwen3-TTS")
    HF_SPACE_TALKING_HEAD: str = os.getenv(
        "HF_SPACE_TALKING_HEAD", "fffiloni/EchoMimic"
    )

    HF_TOKEN_LIVEPORTRAIT: str = os.getenv("HF_TOKEN", "")
    HF_TOKEN_QWEN3_TTS: str = os.getenv("HF_TOKEN", "")
    HF_TOKEN_TALKING_HEAD: str = os.getenv("HF_TOKEN", "")

    ASSETS_ROOT: str = str(BASE_DIR / "assets")


settings = Settings()
