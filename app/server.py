from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
import pandas as pd
import os
import json
from datetime import datetime
from .utils import clean_data,analytics


app = FastAPI()


# Define data directory and file paths
data_dir = 'dataset/'
yellow_files = ['yellow_tripdata_2022-01.parquet', 'yellow_tripdata_2022-02.parquet']
output_dir = 'output/'


# combain the files
df = pd.concat([pd.read_parquet(os.path.join(data_dir, f)) for f in yellow_files])
df = clean_data(df)
metrics = analytics(df)

# Store the metrics in a JSON file
filename = datetime.now().strftime('%Y%m%d') + '_yellow_taxi_kpis.json'
filepath = os.path.join(output_dir, filename)
with open(filepath, 'w') as f:
    json.dump(metrics, f)

@app.get('/')
async def root():
    return {'message': 'Welcome to the NYC Taxi KPIs API!'}

@app.get('/compute_metrics')
async def analytics_api():
    # Load the taxi data
    # ...

    # Clean the data
    # ...

    # Compute the metrics
    metrics = analytics(df)

    # Store the metrics in a JSON file
    filename = datetime.now().strftime('%Y%m%d') + '_yellow_taxi_kpis.json'
    filepath = f'/app/data/{filename}'
    with open(filepath, 'w') as f:
        json.dump(metrics, f)

    return JSONResponse(content=metrics)
