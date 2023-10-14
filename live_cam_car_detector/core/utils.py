import logging
import os.path
from datetime import date, datetime

import cv2

from .constants import LOGS_FOLDER, TMP_DIR

today = date.today()
# Configure logging
logging.basicConfig(
    filename=os.path.join(LOGS_FOLDER, f"{today}_debug.log"),
    level=logging.DEBUG,
    format="%(asctime)-s.%(msecs)03d %(levelname)-6.6s %(filename)-18.18s line:%(lineno)-4.4d %(funcName)-18s %(message)s",
)


def generate_timestamp_now():
    now = datetime.now()
    return now.strftime("%Y_%m_%d__%H_%M_%S")


def crop_cv2_image(original_image, box, folder_path=TMP_DIR):
    x, y, w, h = box
    # Crop the region from the original image
    cropped_region = original_image[y : y + h, x : x + w]

    # Construct the output file path
    output_path = os.path.join(folder_path, f"{generate_timestamp_now()}_.png")

    # Save the cropped region as a PNG image
    cv2.imwrite(output_path, cropped_region)

    return output_path
