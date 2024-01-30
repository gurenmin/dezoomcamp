# dezoomcamp
## clone repo: 
### <> Code -> Clone HTTPS -> https://github.com/gurenmin/dezoomcamp.git

docker run -it \ 
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB=ny_taxi \
-v $(pwd)/ny_taxi_postgres_data:/var/libv/postgresql/data \
-p 5432:5432 \
postgres:13