import asyncio
import json
import logging

import requests

from .utils import logging

post_url = "http://127.0.0.1:8000/api/v1/detections/"

query_url = "http://127.0.0.1:8000/api/v1/detections/ref/"

headers = {"Content-Type": "application/json"}


def package_data(file_path: str):
    return json.dumps({"src_file": f"{file_path}"})


def make_post_request(url, headers, data):
    try:
        response = requests.post(url=url, headers=headers, data=data)

        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        logging.debug(response.text)

        return json.loads(response.text)
    except Exception as e:
        logging.error(f"Error making POST request to {url}: {e}", exc_info=True)
        return None



def make_get_request(url, headers):
    try:
        response = requests.get(url=url, headers=headers)

        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        logging.debug(response.text)

        return json.loads(response.text)
    except Exception as e:
        logging.error(f"Error making GET request to {url}: {e}", exc_info=True)
        return None

async def post_detection(detection):
    data = package_data(detection)
    return make_post_request(post_url, headers, data)

async def query_detection(id_ref):
    return make_get_request(f"{query_url}{id_ref}/", headers)
