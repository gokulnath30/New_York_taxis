from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from datetime import datetime
import pandas as pd
from utils import *
import os,json,threading,schedule


# scheduler for updating dataset
def scheduler():
    schedule.every().day.at("16:36:00").do(update_data)
    while True:
        schedule.run_pending()


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

if not os.path.isdir("dataset"):
    os.mkdir("dataset")

    
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

    return JSONResponse(content={"output":metrics,"download":filepath,"filename":jsonname,"donut":list(metrics["payment_types"].values()),"lable":list(metrics["payment_types"].keys())})


# Get dataset list
@app.get("/get_files")
async def get_files(request: Request):
    global last_update
    return JSONResponse(content={"files":os.listdir('dataset'),"last_update":last_update})

@app.get("/download/{date}")
async def update_files(date: str):
    res = update_data(date)
    return JSONResponse(content=res)

# Load templates file
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
