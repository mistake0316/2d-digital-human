# 2D Digital Human

A FastAPI service that orchestrates multiple HuggingFace Spaces to create a 2D digital human pipeline — combining text-to-speech, talking head generation, and video-driven portrait animation.

## Architecture

```
FastAPI app (src/app.py)
├── Gradio UI  (/gradio)         — tabbed demo for each client
├── /tts                         — Qwen3-TTS
├── /talking_head                — EchoMimic (audio → animated portrait)
├── /video_driven                — LivePortrait (video → animated portrait)
└── /digital_human               — unified endpoint (tts / audio / video mode)

HuggingFace Spaces (remote inference)
├── KlingTeam/LivePortrait       — video-driven face animation
├── Qwen/Qwen3-TTS               — instruction-following TTS
└── fffiloni/EchoMimic           — audio-driven talking head
```

## Requirements

- Python >= 3.13
- A HuggingFace token with access to the relevant Spaces

## Setup

```bash
# Install dependencies
pip install -e .

# Configure environment
cp .env.example .env   # then fill in your values
```

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `HF_TOKEN` | — | HuggingFace API token (used for all spaces) |
| `HF_SPACE_LIVEPORTRAIT` | `KlingTeam/LivePortrait` | LivePortrait HF Space ID |
| `HF_SPACE_QWEN3_TTS` | `Qwen/Qwen3-TTS` | Qwen3-TTS HF Space ID |
| `HF_SPACE_TALKING_HEAD` | `fffiloni/EchoMimic` | EchoMimic HF Space ID |

## Running

```bash
cd src
uvicorn app:app --reload
```

- Swagger UI: `http://localhost:8000/docs`
- Gradio UI: `http://localhost:8000/gradio`

## API Reference

### `POST /tts`

Generate speech from text using Qwen3-TTS.

```json
{
  "text": "Hello, I am your digital assistant.",
  "voice_description": "A calm, professional female voice."
}
```

Returns: `audio/wav`

---

### `POST /talking_head`

Animate a portrait image with an audio file using EchoMimic.

```json
{
  "image_path": "/path/to/avatar.jpg",
  "audio_path": "/path/to/speech.wav"
}
```

Returns: `video/mp4`

---

### `POST /video_driven`

Animate a portrait image driven by a reference video using LivePortrait.

```json
{
  "image_path": "/path/to/avatar.jpg",
  "video_path": "/path/to/driving.mp4"
}
```

Returns: `video/mp4`

---

### `POST /digital_human`

Unified endpoint that supports multiple animation modes.

```json
{
  "avatar": "/path/to/avatar.jpg",
  "mode": "tts | audio | video",

  // mode=tts
  "text": "Hello world",
  "voice_description": "A cheerful male voice",

  // mode=audio
  "audio": "/path/to/audio.wav",

  // mode=video
  "driving_video": "/path/to/video.mp4"
}
```

| Mode | Description |
|---|---|
| `tts` | Generate speech from `text` + `voice_description`, then animate the avatar |
| `audio` | Animate the avatar with a provided audio file |
| `video` | Animate the avatar driven by a reference video |
| `motion` | Planned (not yet implemented) |

Returns: `video/mp4`

## Project Structure

```
src/
├── app.py          # FastAPI application and route definitions
├── model.py        # Pydantic request/response models
├── config.py       # Settings loaded from environment
├── master_ui.py    # Gradio tabbed UI combining all demos
├── assets/         # Sample assets (images, videos)
└── client/
    ├── liveportrait.py   # LivePortrait HF Space client
    ├── qwen3_tts.py      # Qwen3-TTS HF Space client
    ├── talking_head.py   # EchoMimic HF Space client
    ├── faceswap.py       # Face swap client (in progress)
    └── background.py     # Background replacement client (in progress)
```
