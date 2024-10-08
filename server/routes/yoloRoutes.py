from fastapi import APIRouter
from controllers.yoloControllers import detect

router = APIRouter()

# POST      /yolo/detect
router.add_api_route("/detect", methods=["POST"], endpoint=detect)