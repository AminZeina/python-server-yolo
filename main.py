from typing import Annotated
from fastapi.responses import FileResponse
from ultralytics import YOLO

from fastapi import FastAPI, File, HTTPException, UploadFile
from datetime import datetime
import logging
import uvicorn

'''
This is an inital "mock" endpoint for uploading an image for object detection.
The /detect endpoint is used to upload an image, which is then passed through lightly-trained
YOLO model for drones, then returns a json response containing the list of detected objects in 
the image.

Currently, no opitimization is being done and I'm simply using the ultralytics .predict() function.
It's worth noting that the detection itself only typically takes 30-40 ms (shown by result.speed below),
so the majority of time is spend on overhead. So, this likely can and will be improved on in the future.
'''

logger = logging.getLogger('uvicorn')

app = FastAPI()

model = YOLO("yolo_initial.pt")

@app.get("/")
async def home():
    return FileResponse('index.html')

@app.post("/detect")
async def create_upload_file(file: UploadFile):
    logger.info('Detection endpoint hit')
    start = datetime.now()

    logger.info(file.filename)
    logger.info(file.size)
    logger.info(file.headers)
   

    file_location = f"uploaded/{file.filename}"
    with open(file_location, "wb+") as f:
        f.write(file.file.read())
        

    results = model.predict(file_location)

    result = results[0]
    result.save(f'detected/out-{file.filename}')    
    app.state.latest_file = f'detected/out-{file.filename}'
    
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080,reload=True)