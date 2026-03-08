import gradio as gr
from client.liveportrait import demo as liveportrait_demo
from client.qwen3_tts import demo as qwen3_tts_demo
from client.talking_head import demo as talking_head_demo


demo = gr.TabbedInterface(
    [liveportrait_demo, talking_head_demo, qwen3_tts_demo],
    ["LivePortrait", "TalkingHead", "Qwen3-TTS"],
)
