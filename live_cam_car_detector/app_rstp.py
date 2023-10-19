import cv2
import av
import streamlit as st
from aiortc.contrib.media import MediaPlayer, MediaRecorder
from streamlit_webrtc import (
    VideoProcessorBase,
    WebRtcMode,
    WebRtcStreamerContext,
    create_mix_track,
    create_process_track,
    webrtc_streamer,
)

rtsp_url = "rtsp://admin:123456@192.168.1.13:554/unicast/c0/s1/live"

webrtc_ctx = webrtc_streamer(
    key="self",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=None,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False},
)

def main():
    if webrtc_ctx.video_receiver:
        # Initialize the VideoCapture object for IP camera
        global rtsp_url
        cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

        while True:
            # Read frame from IP camera
            ret, frame = cap.read()

            # Display the frame in Streamlit
            if ret:
                #webrtc_ctx.video_receiver.process_frame(frame)
                st.image(frame, channels="BGR")

            # Press 'q' to exit the loop
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Release the VideoCapture object and cleanup
        cap.release()
        cv2.destroyAllWindows()

main()
