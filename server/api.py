from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from dotenv import dotenv_values, load_dotenv
import os

config = dotenv_values()

load_dotenv()

from routes.yoloRoutes import router as yoloRouter

# FastAPI app
app = FastAPI()

# Initialize FastAPI app for api routes
api_app = FastAPI()

origins = os.getenv("CORS_ORIGINS").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_app.include_router(router=yoloRouter, tags=["YOLO"], prefix="/yolo")

app.mount("/api", api_app, name="api")

# Serve build files from client / frontend
app.mount("/", StaticFiles(directory="../build", html=True), name="build")

templates = Jinja2Templates(directory="../build")

# Handle 404 error
@app.exception_handler(404)
async def catch_all(request: Request, exc: HTTPException):
    return templates.TemplateResponse("index.html", {"request": request})
