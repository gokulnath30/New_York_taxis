# NewYork Taxis Dashboard

This is a FastAPI app that provides a simple REST API for managing data.


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

- `GET /items`: Get a list of all items
- `GET /items/{item_id}`: Get an item by ID
- `POST /items`: Create a new item
- `PUT /items/{item_id}`: Update an item by ID
- `DELETE /items/{item_id}`: Delete an item by ID

## Screenshots

![Dashbaord](/static/img/App.png)

## Video

Check out this video to see the app in action:

[![App Demo](https://img.youtube.com/vi/your-video-id-here/0.jpg)](https://www.youtube.com/watch?v=your-video-id-here)
