import logging
import math

import cv2
from ultralytics import YOLO

# object classes and base detection api endpoint
from .constants import classNamesSelection, fullClassNamesCodes
from .utils import *

classCodes = list(fullClassNamesCodes.keys())
classNames = list(fullClassNamesCodes.values())
selectionCodes = list(classNamesSelection.keys())

# model
model = YOLO("yolo-Weights/yolov8n.pt")
# linewidth and thickness

lw = max(round(sum((640, 480)) / 2 * 0.003), 2)  # Line width.
tf = max(lw - 1, 1)  # Font thickness.


# Define a function to process webcam frames and perform car detection
def detect_cars(frame, process_license_flag=False):
    #results = model.predict(frame, stream=True)    
    results = model.predict(frame, stream=True, verbose=False)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = (
                int(x1),
                int(y1),
                int(x2),
                int(y2),
            )  # convert to int values

            # class code
            cls = int(box.cls[0])
            if cls in selectionCodes:
                # put box in cam
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # confidence
                confidence = math.ceil((box.conf[0] * 100)) / 100
                confidence_log = f"Confidence ---> {confidence}"
                logging.info(confidence_log)

                # class name
                class_log = f"Class name --> {classNames[cls]}"
                logging.info(class_log)

                # object details
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = tf

                custom_label = f"{classNames[cls]}:{confidence}"
                cv2.putText(frame, custom_label, org, font, fontScale, color, thickness)

                if (
                    process_license_flag
                    and (cls in classCodes)
                    and (confidence >= 0.5)
                ):
                    detection = crop_cv2_image(frame, [x1, y1, x2, y2])
                    return frame, detection

    return frame, None

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

rtsp_url = "rtsp://admin:123456@192.168.1.13:554/unicast/c0/s1/live"