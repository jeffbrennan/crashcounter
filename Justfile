@dbinit:
    createdb crashcounter -O postgres

@db:
    psql -U postgres -d crashcounter
