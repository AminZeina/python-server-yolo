import os
import requests
from datetime import datetime
from pathlib import Path
import time

#url = "http://127.0.0.1:5000/predictionImages" # using burnsy's inital endpoints
url = "http://127.0.0.1:8080/detect"

img_dir = "test_images"
elapsed_time_list = []

pathlist = Path(img_dir).rglob('*')
for img_path in pathlist:
    with open(img_path, 'rb') as img:
        name_img= os.path.basename(img_path)
        files= {'file': (name_img,img,'multipart/form-data',{'Expires': '0'}) }

        session = requests.Session()
        start_t = datetime.now()
        r = session.post(url,files=files)
        elapsed = (datetime.now() - start_t).total_seconds() * 1000 # in ms
        print(r.status_code)

        try:
            print(r.json())
        except:
            with open("flask_response.png", 'wb') as f:
                f.write(r.content)
        print(f'elapsed time: {elapsed} ms')
        elapsed_time_list.append(elapsed)
    #time.sleep(4) # can use sleep if you want to test the html page visually to see each new image being shown on the page

print("*** tests done ***")
print(f'list of elapased time per request {elapsed_time_list}')
print(f'Average request time: {sum(elapsed_time_list)/ len(elapsed_time_list)}')


'''
Using the faster-RCNN model (burnsy's) endpoints, a full request to response takes roughly 1800 ms for a new image, and then roughly 500 ms for subsequent requests 

Using the YOLO model (main.py in this directory), the same tests take roughly 800ms and then 100ms (for a new image and then subsequent requests, respectively)
'''