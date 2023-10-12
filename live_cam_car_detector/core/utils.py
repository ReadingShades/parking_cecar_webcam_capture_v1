import json
import logging
import os
from datetime import date, datetime

import cv2
import requests

from .constants import TMP_DIR

isExist = os.path.exists(TMP_DIR)
if not isExist:
    os.makedirs(TMP_DIR)

today = date.today()
# Configure logging
logging.basicConfig(
    filename=f"{today}_http_requests.log", level=logging.INFO, format="%(asctime)s - %(message)s"
)


def make_post_request(url, headers, data):
    try:
        response = requests.post(url=url, headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        return response.text
    except Exception as e:
        logging.error(f"Error making POST request to {url}: {e}")
        return None


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


def package_data(file_path: str):
    return json.dumps({"src_file": f"{file_path}"})
