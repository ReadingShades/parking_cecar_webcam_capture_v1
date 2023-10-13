import gradio as gr
import cv2

def process_frame_with_opencv(frame):
    # Your OpenCV processing code here
    # Example: Convert to grayscale
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Create a Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("Prototipo de app de reconocimiento de placas")
    with gr.Row():
        inp = gr.Image(source="webcam", mirror_webcam=False, streaming=True)
        out = gr.Image(interactive=False)
    btn = gr.Button("Run")
    inp.stream(fn=process_frame_with_opencv, inputs=inp, outputs=out)

demo.queue().launch(debug=True, show_api=False)



