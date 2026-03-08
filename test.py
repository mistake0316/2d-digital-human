import requests

resp_sample = requests.post(
    "http://localhost:8000/return_sample_video", json={"mode": "tts", "avatar": "Amy"}
)

# tts
