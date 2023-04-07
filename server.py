from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import pandas as pd
import os,json
from datetime import datetime
from utils import *
import threading
import schedule



def scheduler():
    schedule.every().day.at("16:36:00").do(update_data)
    while True:
        schedule.run_pending()


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Thread for scheduler 
# my_thread = threading.Thread(target=scheduler)
# my_thread.start()


@app.post("/uploadfiles")
async def calculate_metrics(request: Request):
    uploadfiles = ["dataset/"+x for x in list(dict(await request.form()).values())]
    df = pd.concat([pd.read_parquet(f) for f in uploadfiles])
    df = clean_data(df)
    metrics = analytics(df)
    jsonname = datetime.now().strftime('%Y%m%d') + '_yellow_taxi_kpis.json'
    filepath = f'static/output/{jsonname}'

    with open(filepath, 'w') as f:
        json.dump(metrics, f)

    return JSONResponse(content={"output":metrics,"download":filepath,"filename":jsonname,"donut":list(metrics["payment_types"].values())})


# Get dataset list
@app.get("/get_files")
async def get_files(request: Request):
    return JSONResponse(content={"files":os.listdir('dataset')})


# Load Index file
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
