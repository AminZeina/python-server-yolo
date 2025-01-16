from typing import Annotated
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
from pathlib import Path
from fastapi import FastAPI, File, HTTPException, UploadFile
from datetime import datetime
import logging
import uvicorn
from pathlib import Path

'''
This is an inital "mock" endpoint for uploading an image for object detection.
The /detect endpoint is used to upload an image, which is then passed through lightly-trained
YOLO model for drones, then returns a json response containing the list of detected objects in 
the image.

Currently, no opitimization is being done and I'm simply using the ultralytics .predict() function.
It's worth noting that the detection itself only typically takes 30-40 ms (shown by result.speed below),
so the majority of time is spend on overhead. So, this likely can and will be improved on in the future.
'''

BASE_DIR_PATH = Path(__file__).parent
logger = logging.getLogger('uvicorn')

app = FastAPI()

model = YOLO(BASE_DIR_PATH / "yolo8_v5.pt")

# make required directories
Path(BASE_DIR_PATH / "uploaded/").mkdir(exist_ok=True)
Path(BASE_DIR_PATH / "detected/").mkdir(exist_ok=True)


@app.post("/detect")
async def create_upload_file(file: UploadFile):
    logger.info('Detection endpoint hit')
    start = datetime.now()

    logger.info(file.filename)
    logger.info(file.size)
    logger.info(file.headers)
   

    file_location = BASE_DIR_PATH / f"uploaded/{file.filename}"
    with open(file_location, "wb+") as f:
        f.write(file.file.read())
        

    results = model.predict(file_location)

    result = results[0]
    result.save(BASE_DIR_PATH / f'detected/out-{file.filename}')    
    app.state.latest_file = BASE_DIR_PATH / f'detected/out-{file.filename}'
    
    elapsed = datetime.now() - start
    logger.info(f'elapsed time: {elapsed.total_seconds() * 1000}')
    logger.info(f'results.names: {result.names}')
    logger.info(f'results.speed (in ms): {result.speed}')

    return result.to_json()

@app.get("/latest-image")
async def get_latest_image():
    try:
        imagepath = app.state.latest_file
    except AttributeError:
        raise HTTPException(status_code=404, detail="No image found")
    return FileResponse(imagepath)

app.mount("/", StaticFiles(directory= BASE_DIR_PATH / "static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080,reload=True)