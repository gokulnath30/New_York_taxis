import pandas as pd
import os
import json
from datetime import datetime
import urllib.request

# declare payment types
# 

# Filter the data
def clean_data(df):
    print(df)
    df = df[['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'passenger_count', 'trip_distance','fare_amount', 'tip_amount', 'extra', 'payment_type']]
    
    df = df.dropna(how='any')
    df = df[(df.trip_distance > 0) & (df.fare_amount > 0) ]
    return df

# Compute the metrics
def analytics(df):
    payment_types = {
    1: 'Credit card',
    2: 'Cash',
    3: 'No charge',
    4: 'Dispute',
    5: 'Unknown',
    6: 'Voided trip'
    }
    # df['price_per_mile'] = (df.fare_amount + df.tip_amount + df.extra) / df.trip_distance
    df['price_per_mile'] = (df.total_amount) / df.trip_distance
    avg_price_per_mile = df.price_per_mile.mean()
    
    payment_types = df.payment_type.map(payment_types).value_counts().to_dict()

    payment_counts = df['payment_type'].value_counts().to_dict()

    print(payment_counts)
    
    df['custom_indicator'] = (df.tip_amount + df.extra) / df.trip_distance
    custom_indicator = df.custom_indicator.mean()
    
    return {'avg_price_per_mile': avg_price_per_mile,
            'payment_types': payment_types,
            'custom_indicator': custom_indicator}


# # Define data directory and file paths
data_dir = 'dataset/'
yellow_files = ['yellow_tripdata_2022-08.parquet','yellow_tripdata_2022-08.parquet']
# output_dir = 'output/'


# combain the files
# df = pd.concat([pd.read_parquet(os.path.join(data_dir, f)) for f in yellow_files])
# df = clean_data(df)
# metrics = analytics(df)
# print(metrics)

# # Store the metrics in a JSON file
# filename = datetime.now().strftime('%Y%m%d') + '_yellow_taxi_kpis.json'
# filepath = os.path.join(output_dir, filename)
# with open(filepath, 'w') as f:
#     json.dump(metrics, f)


# current_date = datetime.now()
# current_month_date = datetime(current_date.year, current_date.month, 1)
# cmonth = current_month_date.strftime('%Y-%m')

cmonth = "2022-08"
try:
    url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_'+cmonth+'.parquet'
    folder_path = 'dataset/'
    file_name = os.path.basename(url)
    path = os.path.join(folder_path, file_name)
    urllib.request.urlretrieve(url, path)
    
except:
    print(cmonth+" This Month Data Not found")


# import datetime

# def get_month_list(start_year, end_year):
#     start_date = datetime.date(start_year, 1, 1)
#     end_date = datetime.date(end_year, 12, 31)
#     months = []
#     while start_date <= end_date:
#         months.append(start_date.strftime("%Y-%m"))
#         start_date += datetime.timedelta(days=32)
#         start_date = start_date.replace(day=1)
#     return months

# # Example usage
# months = get_month_list(2022, 2023)
# print(months)
