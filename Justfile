@db:
    @docker exec -it $(docker ps --filter "name=crashcounter-crashcounter-db-1" -q) psql -U crashcounter -d crashcounter

@term:
    @docker exec -it $(docker ps --filter "name=crashcounter-airflow-apiserver-1" -q) /bin/bash

@trunc:
    @docker exec -it $(docker ps --filter "name=crashcounter-crashcounter-db-1" -q) \
    psql -U crashcounter -d crashcounter -c " \
        TRUNCATE TABLE person; \
        TRUNCATE TABLE crash; \
        TRUNCATE TABLE vehicle; \
    "

@up:
    @docker compose up --build -d

@down:
    @docker compose down
