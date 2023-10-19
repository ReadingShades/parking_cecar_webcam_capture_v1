import cv2
import asyncio

window_width = 640
window_height = 480

# Number of frames to pool before yielding
pool_size = 10
frame_pool = []

def rtsp_frame_generator(rtsp_url):
    # cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
    cap = cv2.VideoCapture(
        rtsp_url,
    )
    # print(cap.getBackendName())
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, window_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, window_height)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cv2.namedWindow('UNV IP Camera', cv2.WINDOW_NORMAL)  # WINDOW_NORMAL allows resizing
    cv2.resizeWindow('UNV IP Camera', window_width, window_height)
    # print(cap.get(cv2.CAP_PROP_FPS))

    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("Error: Could not read frame.")
                break

            global frame_pool
            frame_pool.append(frame)

            if len(frame_pool) >= pool_size:
                yield frame_pool
                frame_pool = []

    except KeyboardInterrupt:
        # Handle keyboard interrupt gracefully
        pass
    finally:
        cap.release()
        print("Video capture released.")


# Replace 'rtsp://your_rtsp_url' with the actual RTSP URL of your camera.
# rtsp_url = 'rtsp://zephyr.rtsp.stream/pattern?streamKey=3ff519acb958c78851a49242c18ce46a'
rtsp_url = "rtsp://admin:123456@192.168.1.13:554/unicast/c0/s1/live"

# Create a generator for frames
frame_generator = rtsp_frame_generator(rtsp_url)

from core.gradio_detect_wrappers import (
    detect_license_save_wrapper,
    detect_license_nosave_wrapper,
)


# To retrieve frames, you can use a loop like this:
def detection_process():
    for frames in frame_generator:    
        for frame in frames:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            """ frame_rgb, detection = detect_license_save_wrapper(frame_rgb)
            print(detection)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) """
            frame_resized = cv2.resize(frame_rgb, (window_width, window_height))
            frame_resized = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.imshow("UNV IP Camera", frame_resized)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release OpenCV resources and close the display window
    cv2.destroyAllWindows()


detection_process()
