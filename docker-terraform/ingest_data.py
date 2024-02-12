#!/usr/bin/env python
# coding: utf-8

import argparse
import os
from sqlalchemy import create_engine
import pandas as pd
from time import time



def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = str(params.port)
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = 'output.csv'

    print(port)

    #download 
    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

 
    # df = pd.read_csv('taxi+_zone_lookup.csv', nrows=100)
    # df.head(n=0).to_sql(name='taxi_zone_lookup',con=engine,if_exists='replace')
    # df_green = pd.read_csv('green_tripdata_2019-09.csv.gz',nrows=100,compression='gzip')

    # print(pd.io.sql.get_schema(df,name='taxi+_zone_lookup.csv',con=engine))
    # get_ipython().run_line_magic('timeit', "df.to_sql(name='taxi_zone_lookup',con=engine,if_exists='append')")


    #df_green.head(n=0).to_sql(name='green_tripdata_2019',con=engine,if_exists='replace')


    df_iter = pd.read_csv(csv_name,iterator=True,compression='gzip',chunksize=100000)
    df_green = next(df_iter)

    df_green.lpep_pickup_datetime = pd.to_datetime(df_green.lpep_pickup_datetime)
    df_green.lpep_dropoff_datetime= pd.to_datetime(df_green.lpep_dropoff_datetime)

    df_green.head(n=0).to_sql(name=table_name,con=engine,if_exists='replace')

    df_green.to_sql(name=table_name,con=engine,if_exists='append')


    while True:
        t_start = time()  
        df_green = next(df_iter)
        df_green.lpep_pickup_datetime = pd.to_datetime(df_green.lpep_pickup_datetime)
        df_green.lpep_dropoff_datetime= pd.to_datetime(df_green.lpep_dropoff_datetime)
        df_green.to_sql(name=table_name,con=engine,if_exists='append')    
        t_end = time()
        print('inserted another chunk, took %.3f second' %(t_end-t_start))
        


    # query1 = """
    # select count(1) from green_tripdata_2019 limit 10
    # """
    # pd.read_sql(query1, con=engine)

    # query1 = """
    # select * from taxi_zone_lookup where "Zone" ='Astoria' limit 10
    # """
    # pd.read_sql(query1, con=engine)


    # query = """
    # select zone2."Zone",sum(tip_amount) from green_tripdata_2019 trip
    # join taxi_zone_lookup zone2 on trip."DOLocationID" =zone2."LocationID"
    # where "PULocationID" =7 and substring(lpep_pickup_datetime,0,8) ='2019-09'
    # group by zone2."Zone" order by sum(tip_amount) desc limit 20
    # """
    # pd.read_sql(query, con=engine)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to postgresql')
    # user
    # password
    # host
    # port
    # database name
    # tablename
    # url of the csv

    parser.add_argument('--user',help ='username for postgres')
    parser.add_argument('--password',help ='password for postgres')
    parser.add_argument('--host',help ='host for postgres')
    parser.add_argument('--port',help ='port for postgres')
    parser.add_argument('--db',help ='database name for postgres')
    parser.add_argument('--table_name',help ='name of the table')
    parser.add_argument('--url',help ='url of the csv file')

    args = parser.parse_args()

    main(args)