# NewYork Taxis Dashboard

The Application computing various statistics from the dataset of New York taxis trips. Specifically, processing the Yellow taxi trips data and computing the following metrics.


## Clone Repo
    git clone https://github.com/gokulnath30/New_York_taxis
    cd New_York_taxis
    pip install -r requirements.txt
    run_server.cmd or py -m uvicorn server:app --reload

## Docker Installation

    docker build -t my-fastapi-app .
    docker run -d --name my-app-container -p 80:80 my-fastapi-app

This will start the app at http://localhost:8000. You can then use the API to manage data.

## API Endpoints

The following API endpoints are available:

- `GET /download/2023-01`: Download dataset 
- `GET /get_files`: Load current files from server
- `POST /uploadfiles`: Calculate Metrices

## Deployed in Render

[https://new-york-taxis.onrender.com/](https://new-york-taxis.onrender.com/ "NewYork Taxis")


## Screenshots

![Dashbaord](/static/img/App.png)

## Video
Check out this video to see the app in action:

[![App Demo](https://img.youtube.com/vi/BEXRY6RowWM/0.jpg)](https://youtu.be/BEXRY6RowWM)
