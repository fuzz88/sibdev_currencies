#!/bin/sh

docker compose exec -ti postgres bash -c "su -c psql postgres"