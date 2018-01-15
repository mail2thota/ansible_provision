#!/bin/bash

if psql -U postgres -lqt | cut -d \| -f 1 | grep -qw postgres; then
    echo "Postgres Test Success"
else
    echo "Postgres Test Failed"
fi
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
