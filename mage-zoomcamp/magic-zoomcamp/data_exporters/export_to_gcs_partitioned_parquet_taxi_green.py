import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


# config_path = path.join(get_repo_path(), 'io_config.yaml')
# config_profile = 'dev'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/my-creds.json"
bucket_name ="helpful-symbol-412902-terraform-bucket"
project_id = "helpful-symbol-412902"

table_name ="nyc_taxi_green_data"

root_path = f'{bucket_name}/{table_name}'

@data_exporter
def export_data(data, *args, **kwargs):
    #data['lpep_pickup_date'] =data['lpep_pickup_datetime'].dt.date

    table = pa.Table.from_pandas(data)
    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols =['lpep_pickup_date'],
        filesystem=gcs
    )
