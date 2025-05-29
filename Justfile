@dbinit:
    createdb crashcounter -O postgres

@db:
    psql -U postgres -d crashcounter

@trunc:
    psql -U postgres -d crashcounter -c "TRUNCATE TABLE person; TRUNCATE TABLE crash; TRUNCATE TABLE vehicle;"
