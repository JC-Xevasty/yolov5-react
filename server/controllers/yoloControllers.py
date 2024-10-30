from fastapi.responses import JSONResponse
from pydantic import BaseModel

# For converting base64 string to an image
import numpy as np
import base64
import cv2

# For converting image to base64 string
from PIL import Image
import io

# For model
from ultralytics import YOLO
import torch

# Load the YOLOv5 model
# model = YOLO("models/yolov5su.pt")
model = torch.hub.load("ultralytics/yolov5", "custom", path="models/yolov5s.pt")

"""
@desc     Upload a single dataset
route     POST api/yolo/detect
@access   Private
"""


class DetectRequest(BaseModel):
    image_uri: str


async def detect(request: DetectRequest):
    # Get data uri
    encoded_data = request.image_uri.split(",")[1]

    # Create numpy array after decoding data uri
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)

    # Convert numpy array to an image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Run in model
    result = model(img)

    # Get the numpy array of the annotated image
    # Using YOLO to load model
    # result_nparr = result[0].plot()
    
    # Using torch to load model
    result.render() # Render the detections (this updates results.imgs with the annotated images)
    
    # Get the annotated image from result.ims (in BGR format)
    annotated_image = result.ims[0]
    
    # Optional: If you want to convert it to RGB (since OpenCV user BGR by default)
    annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
    
    result_nparr = annotated_image_rgb
    
    # Convert numpy array to base64 string.
    data = Image.fromarray(result_nparr)
    data_bytes = io.BytesIO()
    data.save(data_bytes, "JPEG")
    data64 = base64.b64encode(data_bytes.getvalue())
    result_image_as_base64_string = "data:img/jpeg;base64," + data64.decode("utf-8")

    # Return result
    return JSONResponse(content={"result_image": result_image_as_base64_string})
