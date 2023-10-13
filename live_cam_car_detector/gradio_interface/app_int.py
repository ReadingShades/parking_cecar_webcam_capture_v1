import gradio as gr

from .frame_detection_utils import *


def set_gr_w648_h480_ninteractive():
    return gr.Image(shape=(640, 480), interactive=False)


# Create a Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("Prototipo de app de reconocimiento de placas")
    with gr.Row():
        video_feed = gr.Image(
            shape=(640, 480), source="webcam", mirror_webcam=False, streaming=True
        )
        live_vehicle_detection_cam = set_gr_w648_h480_ninteractive()
    btn_detect = gr.Button("Detect")
    with gr.Row():
        with gr.Column():
            gr.Markdown("license_detection")
            license_detection_img = set_gr_w648_h480_ninteractive()
        with gr.Column():
            gr.Markdown("license_crop")
            license_detection_crop = set_gr_w648_h480_ninteractive()
            ocr_output = gr.TextArea(interactive=False)

    # EventListeners
    video_feed.stream(
        fn=detect_cars, 
        inputs=video_feed, 
        outputs=[live_vehicle_detection_cam, _]
    )
    btn_detect.click(
        fn=detect_license,
        inputs=video_feed,
        outputs=[
            license_detection_img, 
            license_detection_crop, 
            ocr_output
            ],
        show_progress=True
    )

demo.queue().launch(debug=True, show_api=False)
