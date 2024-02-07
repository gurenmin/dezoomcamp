# dezoomcamp
## clone repo: 
### <> Code -> Clone HTTPS -> https://github.com/gurenmin/dezoomcamp.git
docker network create pg-network
docker rm pg-database
docker ps

docker run -it -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" -e POSTGRES_DB=ny_taxi -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data -p 5432:5432 --network=pg-network --name pg-database postgres:13

docker start pg-database
docker rm pg-database -f

docker run -it -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" -e PGADMIN_DEFAULT_PASSWORD="root" -p 8080:80	 --network=pg-network --name pgadmin dpage/pgadmin4

docker start pgadmin
docker rm pgadmin -f

pgcli -h localhost -p 5432 -u root -d ny_taxi

jupyter nbconvert --to python 'update-data.ipynb'

URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"


python ingest_data.py \
--user=root \
--password=root \
--host=localhost \
--port=5432 \
--db=ny_taxi \
--table_name=yellow_taxi_trip \
--url=${URL}


docker build -t taxt_ingext:v0001 .

docker run -it --network=pg-network \
taxt_ingext:v0001 \
--user=root \
--password=root \
--host=pg-database \
--port=5432 \
--db=ny_taxi \
--table_name=yellow_taxi_trip \
--url=${URL}

python -m http.server
