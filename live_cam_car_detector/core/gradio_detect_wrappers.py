import asyncio

from .detection_api import post_detection, query_detection
from .utils import logging
from .vehicle_video_stream_detector import detect_cars, rtsp_frame_generator


async def detect_license(frame, save_img_flag):
    frame, detection = detect_cars(frame, save_img_flag)
    # breakpoint()

    if detection is not None:
        try:
            query_data = await post_detection(detection=detection)
        except Exception as e:
            logging.error(e, exc_info=True)

    return query_data.get("id_ref")
    #return "test"

def detect_license_save_wrapper(frame):
    return detect_cars(frame, True)

def detect_license_nosave_wrapper(frame):
    return detect_cars(frame, False)

async def query_detection_by_reference(id_ref):
    try:
        license_detection_data = await query_detection(id_ref=id_ref)
    except Exception as e:
        logging.error(e, exc_info=True)
    # breakpoint()
    if license_detection_data is not None:
        return (
            license_detection_data.get("pred_loc"),
            license_detection_data.get("crop_loc"),
            license_detection_data.get("ocr_text_result"),
        )
