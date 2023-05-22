#!/bin/bash

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE feed;

EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "feed" <<-EOSQL
    CREATE TABLE activity(
        avtivity_id SERIAL PRIMARY KEY,
        username TEXT NOT NULL,
        description TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL default now()
    );

EOSQL
