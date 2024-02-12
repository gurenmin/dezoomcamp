import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    #response = requests.get(url)
    #return pd.read_csv(io.StringIO(response.text), sep=',')
    taxi_dytpes = {
                    'VendorID': pd.Int64Dtype(),
                    'store_and_fwd_flag': str,
                    'RatecodeID': pd.Int64Dtype(),
                    'PULocationID': pd.Int64Dtype(),
                    'DOLocationID': pd.Int64Dtype(),
                    'passenger_count': pd.Int64Dtype(),
                    'trip_distance': float,
                    'fare_amount': float,
                    'extra': float,
                    'mta_tax': float,
                    'tip_amount': float,
                    'tolls_amount': float,
                    'ehail_fee': float,
                    'improvement_surcharge': float,
                    'total_amount': float,
                    'payment_type': pd.Int64Dtype(),
                    'trip_type': pd.Int64Dtype(),
                    'congestion_surcharge': float 
                }

    parse_dates = ['lpep_pickup_datetime','lpep_dropoff_datetime']
    pd_green = pd.DataFrame()
    for i in range(10,13):
        url = (f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-{i}.csv.gz")
        if not pd_green.empty:
            pd_green = pd.concat([pd_green,pd.read_csv(url, sep=",", compression="gzip", dtype=taxi_dytpes, parse_dates=parse_dates)])
        else:
            pd_green = pd.read_csv(url, sep=",", compression="gzip", dtype=taxi_dytpes, parse_dates=parse_dates)
        
    return pd_green


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
