#!/bin/bash

# Check if required environment variables are set
if [ -z "$POSTGRES_PASSWORD" ]; then
    echo "Error: POSTGRES_PASSWORD environment variable is not set."
    exit 1
fi

if [ -z "$POSTGRES_USER" ]; then
    echo "Error: POSTGRES_USER environment variable is not set."
    exit 1
fi

if [ -z "$POSTGRES_API_USER" ]; then
    echo "Error: POSTGRES_API_USER environment variable is not set."
    exit 1
fi

if [ -z "$POSTGRES_API_PASSWORD" ]; then
    echo "Error: POSTGRES_API_PASSWORD environment variable is not set."
    exit 1
fi

if [ -z "$POSTGRES_API_DATABASE" ]; then
    echo "Error: POSTGRES_API_DATABASE environment variable is not set."
    exit 1
fi

echo "Creating role '$POSTGRES_API_USER' and database '$POSTGRES_API_DATABASE'..."
PGPASSWORD="$POSTGRES_PASSWORD" psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE ROLE $POSTGRES_API_USER WITH LOGIN PASSWORD '$POSTGRES_API_PASSWORD';
    CREATE DATABASE $POSTGRES_API_DATABASE WITH OWNER $POSTGRES_API_USER;
EOSQL

# Check if psql command was successful
if [ $? -ne 0 ]; then
    echo "Error: Database initialization failed."
    exit 1
fi

echo "Granting read and write permissions to role '$POSTGRES_API_USER' on tables in schema 'public' of database '$POSTGRES_API_DATABASE'..."
PGPASSWORD="$POSTGRES_PASSWORD" psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname="$POSTGRES_API_DATABASE" <<-EOSQL
    -- Revoke connect privilege from all databases
    REVOKE CONNECT ON DATABASE postgres FROM $POSTGRES_API_USER;
    REVOKE CONNECT ON DATABASE postgres FROM PUBLIC;

    -- Grant connect privilege to the specific API database
    GRANT CONNECT ON DATABASE $POSTGRES_API_DATABASE TO $POSTGRES_API_USER;

    -- Grant table-level permissions in the specific database
    \connect $POSTGRES_API_DATABASE
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO $POSTGRES_API_USER;

    -- Ensure default privileges for new tables
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO $POSTGRES_API_USER;
EOSQL

# Check if psql command was successful
if [ $? -ne 0 ]; then
    echo "Error: Granting permissions failed."
    exit 1
fi
