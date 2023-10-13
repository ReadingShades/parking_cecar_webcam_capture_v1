import logging
import math
import time

import cv2
from ultralytics import YOLO

from core.utils import *

# object classes and base detection api endpoint
from core.constants import classNamesSelection, fullClassNamesCodes, headers, url

classCodes = list(fullClassNamesCodes.keys())
classNames = list(fullClassNamesCodes.values())

# model
model = YOLO("yolo-Weights/yolov8n.pt")


# Define a function to process webcam frames and perform car detection
def detect_cars(frame, process_license_flag=False):
    results = model.predict(frame, stream=True)

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
            if cls in classNamesSelection:
                # put box in cam
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # confidence
                confidence = math.ceil((box.conf[0] * 100)) / 100
                print("Confidence --->", confidence)

                # class name
                print("Class name -->", classNames[cls])

                # object details
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2

                # cv2.putText(frame, classNames[cls], org, font, fontScale, color, thickness)
                custom_label = f"{classNames[cls]}:{confidence}"
                cv2.putText(frame, custom_label, org, font, fontScale, color, thickness)

                """ # make async query and logg it
                if confidence >= 0.6:
                    data = package_data(crop_cv2_image(frame, [x1, y1, x2, y2]))
                    future = executor.submit(make_post_request, url, headers, data)
                    logging.info(data)

                    if future_result := future.result():
                        logging.info(f"POST request response: {future_result}")
                        future = None """

    return frame

def post_detection():
    pass
