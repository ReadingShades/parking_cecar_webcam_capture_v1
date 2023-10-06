import json
import os
from datetime import datetime

import cv2

from .constants import TMP_DIR

isExist = os.path.exists(TMP_DIR)
if not isExist:
    os.makedirs(TMP_DIR)


def generate_timestamp_now():
    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d__%H_%M_%S")
    return dt_string


def crop_cv2_image(original_image, box, folder_path=TMP_DIR):
    x, y, w, h = box
    # Crop the region from the original image
    cropped_region = original_image[y : y + h, x : x + w]

    # Construct the output file path
    output_path = os.path.join(original_image, f"{generate_timestamp_now()}_.png")

    # Save the cropped region as a PNG image
    cv2.imwrite(output_path, cropped_region)

    return output_path


def package_data(file_path: str):
    data = json.dumps({"src_file": f"{file_path}"})
    return data
