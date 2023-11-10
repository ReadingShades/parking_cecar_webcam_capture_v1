import gradio as gr

from .gradio_detect_wrappers import *


css = """
"""

# Create a Gradio interface
with gr.Blocks(css=css) as demo:
    # Top section of the application
    gr.Markdown("# Prototipo de app de reconocimiento de placas")
    with gr.Row():
        video_feed = gr.Image(
            shape=(720, 600),
            type="numpy",
            source="webcam",
            mirror_webcam=False,
            streaming=True,
            show_label=False,
        )
        live_vehicle_detection_cam = gr.Image(
            shape=(720, 600), interactive=False, show_label=False
        )
    with gr.Row():
        switch_save_frame = gr.Radio(
            [("No", 0), ("Yes", 1)],
            value=0,
            label="Save frame?",
            info="Switches the capture frame mode between NO and YES",
        )
        dump_output = gr.State(value=0)

    # EventListeners
    video_feed.stream(
        fn=detect_license_switch_wrapper,
        inputs=[video_feed, switch_save_frame],
        outputs=[live_vehicle_detection_cam, dump_output],
    )


demo.queue().launch(debug=True, show_api=False)
