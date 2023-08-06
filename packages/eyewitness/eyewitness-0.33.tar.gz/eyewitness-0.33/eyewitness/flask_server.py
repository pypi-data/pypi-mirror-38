import io

from flask import Flask
from flask import request

from eyewitness.image_id import ImageId
from eyewitness.image_utils import ImageHandler


class ObjectDetectionFlaskWrapper(object):
    def __init__(self, obj_detector, detection_result_handler):
        app = Flask(__name__)
        self.app = app
        self.obj_detector = obj_detector
        self.detection_result_handler = detection_result_handler

        @app.route("/detect_post_bytes", methods=['POST'])
        def detect_image_bytes_objs():
            image_id = ImageId.from_str(request.headers['image_id'])

            raw_image_path = request.headers.get('raw_image_path', None)

            # read data from Bytes
            data = request.data
            image_data_raw = io.BytesIO(bytearray(data))
            image_raw = ImageHandler.read_image_bytes(image_data_raw)

            if raw_image_path:
                ImageHandler.save(image_raw, raw_image_path)

            # detect objs
            detection_result = self.obj_detector.detect(image_raw, image_id)
            detection_result_handler.handle(detection_result)
            return "successfully detected"

        @app.route("/detect_post_path", methods=['POST'])
        def detect_image_file_objs():
            image_id = ImageId.from_str(request.headers['image_id'])
            raw_image_path = request.headers['raw_image_path']
            image_raw = ImageHandler.read_image_file(raw_image_path)
            detection_result = self.obj_detector.detect(image_raw, image_id)
            detection_result_handler.handle(detection_result)
            return "successfully detected"
