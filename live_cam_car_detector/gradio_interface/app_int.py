import gradio as gr

from .frame_detection_utils import *


css = """
"""

# Create a Gradio interface
with gr.Blocks(css=css) as demo:
    gr.Markdown("# Prototipo de app de reconocimiento de placas")
    with gr.Row():
        video_feed = gr.Image(
            shape=(640, 480),
            type="numpy",
            source="webcam",
            mirror_webcam=False,
            streaming=True,
        )
        toggle_save_img = gr.State(True)
        live_vehicle_detection_cam = gr.Image(shape=(640, 480), interactive=False)
        # dump_output = gr.Text(interactive=False, visible=False)
        dump_output = gr.Text(interactive=False)
    btn_detect = gr.Button("Detect")
    with gr.Row():
        with gr.Column():
            gr.Markdown("### license_detection")
            license_detection_img = gr.Image(shape=(640, 480), interactive=False)
        with gr.Column():
            gr.Markdown("### license_crop")
            license_detection_crop = gr.Image(shape=(640, 480), interactive=False, show_label=False)
            ocr_output = gr.TextArea(lines=4, max_lines=10, interactive=False)
        with gr.Column():
            gr.Markdown("#### reference id:")
            detection_reference = gr.Text(lines=1, max_lines=1)
            btn_query = gr.Button("Search_detection")

    # EventListeners
    video_feed.stream(
        fn=detect_cars,
        inputs=video_feed,
        outputs=[live_vehicle_detection_cam, dump_output],
    )
    btn_detect.click(
        fn=detect_license,
        inputs=[video_feed, toggle_save_img],
        outputs=detection_reference,
        show_progress=True,
    )
    btn_query.click(
        fn=query_detection_by_reference,
        inputs=detection_reference,
        outputs=[license_detection_img, license_detection_crop, ocr_output],
        show_progress=True,
    )

demo.queue().launch(debug=True, show_api=False)
