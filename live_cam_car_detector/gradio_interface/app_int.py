import gradio as gr
import cv2

from .frame_detection_utils import *

# Create a Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("Prototipo de app de reconocimiento de placas")
    with gr.Row():
        inp = gr.Image(source="webcam", mirror_webcam=False, streaming=True)
        out = gr.Image(interactive=False)
    btn = gr.Button("Run")
    inp.stream(fn=detect_cars, inputs=inp, outputs=out)

demo.queue().launch(debug=True, show_api=False)
