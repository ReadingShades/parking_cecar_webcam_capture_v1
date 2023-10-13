import pdb
import asyncio
import logging
import math

import cv2

# object classes and base detection api endpoint
from core.constants import (
    classNamesSelection,
    fullClassNamesCodes,
    headers,
    post_url,
    query_url,
)
from core.utils import *
from ultralytics import YOLO

classCodes = list(fullClassNamesCodes.keys())
classNames = list(fullClassNamesCodes.values())

# model
model = YOLO("yolo-Weights/yolov8n.pt")
# linewidth and thickness

lw = max(round(sum((640, 480)) / 2 * 0.003), 2)  # Line width.
tf = max(lw - 1, 1)  # Font thickness.


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

                # cv2.putText(frame, classNames[cls], org, font, fontScale, color, thickness)
                custom_label = f"{classNames[cls]}:{confidence}"
                cv2.putText(frame, custom_label, org, font, fontScale, color, thickness)

                if confidence >= 0.5 and process_license_flag:
                    detection = crop_cv2_image(frame, [x1, y1, x2, y2])
                    return frame, detection

    return frame, None


async def post_detection(detection):
    data = package_data(detection)
    return make_post_request(post_url, headers, data)


async def query_detection(id_ref):
    return make_get_request(f"{query_url}{id_ref}/", headers)


async def detect_license(frame, save_img_flag):
    img, detection = detect_cars(frame, save_img_flag)
    breakpoint()
    if detection is not None:
        try:
            query_data = await post_detection(detection=detection)
        except Exception as e:
            logging.error(exc_info=e)
        breakpoint()
        try:
            license_detection_data = await query_detection(query_data.get("id_ref"))
        except Exception as e:
            logging.error(exc_info=e)
        breakpoint()
        return (
            license_detection_data.get("pred_loc"),
            license_detection_data.get("crop_loc"),
            license_detection_data.get("ocr_text_result"),
        )
