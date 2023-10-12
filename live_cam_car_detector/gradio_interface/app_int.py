import gradio as gr

from .frame_detection_utils import detect_cars

# Create a Gradio interface
iface = gr.Interface(
    fn=detect_cars,
    inputs="webcam",
    outputs="image",  # Output will be an image (processed video frame)
    capture_session=True  # This is important for continuous webcam streaming
)

# Launch the Gradio interface
iface.launch()