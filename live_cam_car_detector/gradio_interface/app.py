import gradio as gr


demo = gr.Blocks(analytics_enabled=True)

with demo:
    with gr.Row():
        web_input = gr.Image(
                            source="webcam",
                            type="pil",
                            shape=(150, 150),
                            streaming=True,
                            mirror_webcam=False,
                        )
    with gr.Row():
        web_input_2 = gr.Image(
                            source="webcam",
                            type="pil",
                            shape=(150, 150),
                            streaming=True,
                            mirror_webcam=False,
                        )

demo.launch(debug=True, enable_queue=True, show_api=False)
