import cv2

def rtsp_frame_generator(rtsp_url):
    width = 640
    height = 480
    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
    #print(cap.getBackendName())
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, 30)
    #print(cap.get(cv2.CAP_PROP_FPS))

    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("Error: Could not read frame.")
                break

            yield frame

    except KeyboardInterrupt:
        # Handle keyboard interrupt gracefully
        pass
    finally:
        cap.release()
        print("Video capture released.")

# Replace 'rtsp://your_rtsp_url' with the actual RTSP URL of your camera.
rtsp_url = 'rtsp://zephyr.rtsp.stream/pattern?streamKey=3ff519acb958c78851a49242c18ce46a'

# Create a generator for frames
frame_generator = rtsp_frame_generator(rtsp_url)

# To retrieve frames, you can use a loop like this:
for frame in frame_generator:
    cv2.imshow('RTSP Frame', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release OpenCV resources and close the display window
cv2.destroyAllWindows()