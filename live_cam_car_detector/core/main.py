import concurrent.futures
import logging
import math
import time

import cv2
import requests
from ultralytics import YOLO

from .utils import *

# cycle clock in seconds
cycle_pause_duration = 3
cycle_clock_start = 0
cycle_clock_current = 0
# post_func_pause clock in seconds
post_func_pause_duration = 5
post_func_clock_start = 0
post_func_clock_current = 0
# switch that controls wether to reset or not start timer
post_func_sw = 0

# Concurrent adjustment
future = None

# Configure logging
logging.basicConfig(
    filename="http_requests.log", level=logging.INFO, format="%(asctime)s - %(message)s"
)


def make_post_request(url, headers, data):
    try:
        response = requests.post(url=url, headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        return response.text
    except Exception as e:
        logging.error(f"Error making POST request to {url}: {e}")
        return None


with concurrent.futures.ThreadPoolExecutor() as executor:
    # start webcam
    print(cv2.__version__)
    width = 640
    height = 480
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cam.set(cv2.CAP_PROP_FPS, 30)

    # object classes
    from .constants import classNamesSelection, data, fullClassNamesCodes, headers, url

    classCodes = list(fullClassNamesCodes.keys())
    classNames = list(fullClassNamesCodes.values())

    # model
    model = YOLO("yolo-Weights/yolov8n.pt")

    # from here
    while True:
        post_func_clock_current = time.time()        
        success, img = cam.read()
        results = model.predict(img, stream=True)

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
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

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

                    # cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
                    custom_label = f"{classNames[cls]}:{confidence}"
                    cv2.putText(
                        img, custom_label, org, font, fontScale, color, thickness
                    )

                    # make async query and logg it
                    if confidence >= 0.67:
                        data = package_data(crop_cv2_image(img, [x1, y1, x2, y2]))
                        future = executor.submit(make_post_request, url, headers, data)
                        if (post_func_clock_current - post_func_clock_start < post_func_pause_duration):
                            post_func_sw = 1
                        if post_func_sw == 1:
                            post_func_sw = 0
                            post_func_clock_current = 0
                            post_func_clock_start = time.time()

                    if future is not None:
                        result = future.result()
                        if result:
                            logging.info(f"POST request response: {result}")

        cv2.imshow("Webcam", img)
        time.sleep(1)
        print(f"post_func_start = {post_func_clock_start}")
        print(f"post_func_current = {post_func_clock_current}")
        if cv2.waitKey(1) == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()
