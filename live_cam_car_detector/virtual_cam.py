import cv2
import pyvirtualcam
import logging

#print("Starting pyvirtualcam RTSP script...")

# RTSP URL for your video feed
rtsp_url = "rtsp://admin:123456@192.168.1.13:554/unicast/c0/s1/live"

# Initialize the capture from the RTSP stream
cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

# Create a virtual camera
with pyvirtualcam.Camera(width=1260, height=720, fps=20) as cam:
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Resize the frame to match the virtual camera's resolution
            frame = cv2.resize(frame, (1260, 720))

            # Send the frame to the virtual camera
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cam.send(frame_rgb)

            # Show the frame (optional)
            cv2.imshow("RTSP to Virtual Webcam", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except Exception as e:
        #print("pyvirtualcam script crashed with errors...")
        logging.debug(e, exc_info=True)

    #print("Stopping pyvirtualcam...")
    cv2.destroyAllWindows()
