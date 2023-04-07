from datetime import datetime,timedelta
import urllib.request
import os

last_update = datetime.now().strftime("%y-%B-%d %H:%M")

# Filter the data
def clean_data(df):
    df = df[['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'passenger_count', 'trip_distance','fare_amount', 'tip_amount', 'extra', 'payment_type']]
    df = df.dropna(how='any')
    df = df[(df.trip_distance > 0) & (df.fare_amount > 0) ]
    return df

# analysis the metrics
def analytics(df):
    df['price_per_mile'] = (df.fare_amount + df.tip_amount + df.extra) / df.trip_distance
    avg_price_per_mile = df.price_per_mile.mean()

    # declare payment types
    payment_types = {
        1: 'Credit card',
        2: 'Cash',
        3: 'No charge',
        4: 'Dispute',
        5: 'Unknown',
        6: 'Voided trip'
    }
    payment_types = df.payment_type.map(payment_types).value_counts().to_dict()
    
    df['custom_indicator'] = (df.tip_amount + df.extra) / df.trip_distance
    custom_indicator = df.custom_indicator.mean()
    
    return {'avg_price_per_mile': round(avg_price_per_mile,2),
            'payment_types': payment_types,
            'custom_indicator': round(custom_indicator,2)}


def update_data(date=None):
    global last_update
    last_update = datetime.now().strftime("%y-%B-%d %H:%M")
    current_date = datetime.now()
    current_month_date = datetime(current_date.year, current_date.month, 1)
    if date == None:
        cmonth = current_month_date.strftime('%Y-%m')
    else:
        cmonth = date
    # mlist = ['2022-01', '2022-02', '2022-03', '2022-04', '2022-05', '2022-06', '2022-07', '2022-08', '2022-09', '2022-10', '2022-11', '2022-12', '2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06', '2023-07', '2023-08', '2023-09', '2023-10', '2023-11', '2023-12']
    # for cmonth in mlist:

    try:
        url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_'+cmonth+'.parquet'
        folder_path = 'dataset/'
        file_name = os.path.basename(url)
        path = os.path.join(folder_path, file_name)
        urllib.request.urlretrieve(url, path)
        return {"data":"completed"}
    except:
        print(cmonth+" This Month Data Not found")
        return {"data":"not completed"}

