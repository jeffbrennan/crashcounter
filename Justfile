@db:
    @docker exec -it $(docker ps --filter "name=crashcounter-crashcounter-db-1" -q) psql -U crashcounter -d crashcounter

@trunc:
    psql -U postgres -d crashcounter -c "TRUNCATE TABLE person; TRUNCATE TABLE crash; TRUNCATE TABLE vehicle;"
