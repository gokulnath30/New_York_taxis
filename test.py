import pandas as pd
import os
import json
from datetime import datetime


# declare payment types
payment_types = {
    1: 'Credit card',
    2: 'Cash',
    3: 'No charge',
    4: 'Dispute',
    5: 'Unknown',
    6: 'Voided trip'
}

# Filter the data
def clean_data(df):
    df = df[['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'passenger_count', 'trip_distance','fare_amount', 'tip_amount', 'extra', 'payment_type']]
    df = df.dropna(how='any')
    df = df[(df.trip_distance > 0) & (df.fare_amount > 0) ]
    return df

# Compute the metrics
def analytics(df):
    df['price_per_mile'] = (df.fare_amount + df.tip_amount + df.extra) / df.trip_distance
    avg_price_per_mile = df.price_per_mile.mean()
    
    payment_types = df.payment_type.map(payment_types).value_counts().to_dict()
    
    df['custom_indicator'] = (df.tip_amount + df.extra) / df.trip_distance
    custom_indicator = df.custom_indicator.mean()
    
    return {'avg_price_per_mile': avg_price_per_mile,
            'payment_types': payment_types,
            'custom_indicator': custom_indicator}


# Define data directory and file paths
data_dir = 'data/'
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
