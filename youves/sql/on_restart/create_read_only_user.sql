DO $do$ BEGIN IF NOT EXISTS (
    SELECT
    FROM pg_catalog.pg_roles -- SELECT list can be empty for this
    WHERE rolname = 'grafanareader'
) THEN CREATE ROLE grafanareader LOGIN PASSWORD 'password';
END IF;
END $do$;
GRANT CONNECT ON DATABASE dipdup TO grafanareader;
GRANT USAGE ON SCHEMA public TO grafanareader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO grafanareader;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO grafanareader;