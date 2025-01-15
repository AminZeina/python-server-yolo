# Drone Detection Server using YOLO

This project consists of a `./frontend/` and a `./backend/`, which must both be running to use this server



## Structure 
### Frontend
- The frontend is built using React and provides a simple interface for the drone detection server

### Backend
- The backend is built using Python and FastAPI, and hosts a YOLO modelled custom trained for drone detection
- The backend provides a few HTTP endpoints for interacting with the model:
    - `/detect`: POST which requires an image as a file, and returns the model's analysis of the image in JSON format
    - `/latest-image`: GET which returns the visualized analysis of the most recently uploaded image from the `/detect` endpoint. The image returned by this endpoint will show the most recent image with bounding boxes around each detected drone.
- The backend also contains `testRequests.py` which is a script that can be used to test the backend server
    - this script sends a series of requests (one for each image within the `/backend/test_images/` directory) to the server's `/detect` endpoint, and prints the response from the server

## Dependencies
- Python, required to run the backend
    - Any required Python packages are listed in `./backend/requirements.txt` and can be installed using `pip install -r ./backend/requirements.txt`
- Node.js, required to run the frontend
    - Node.js can be downloaded and install from [here](https://nodejs.org/en)

## Running the project 
- To run the project, you must run the FastAPI backend and the React frontend simultaneously. To do that:
1. from `./backend/`, run `main.py`
2. from `./frontend/`, run `npm install`, then run `npm run dev`

- The backend server will now be running at http://localhost:8080, and the React frontend will be running at http://localhost:5173. 


