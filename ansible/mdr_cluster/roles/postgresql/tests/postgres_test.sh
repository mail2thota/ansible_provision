#!/bin/bash

if psql -U postgres -lqt | cut -d \| -f 1 | grep -qw postgres; then
    echo "Postgres Test Success"
else
    echo "Postgres Test Failed"
fi
sudo psql -U postgres -c "ALTER USER postgres PASSWORD 'postgres';"
