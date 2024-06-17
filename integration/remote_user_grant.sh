sudo su postgres
psql
CREATE USER drfadul WITH PASSWORD '*********';


sudo vim /etc/postgresql/14/main/pg_hba.conf
ADD THE FOLLOWING:
host    all             drfadul         0.0.0.0/0               md5


sudo vim /etc/postgresql/14/main/postgresql.conf 
ADD THE FOLLOWING:
listen_addresses = '*'



-- Connect to PostgreSQL as a superuser (e.g., postgres)
\c postgres

-- Grant all privileges on the database synaia to drfadul
GRANT ALL PRIVILEGES ON DATABASE synaia TO drfadul;

-- Connect to the synaia database to grant privileges on its objects
\c synaia

-- Grant all privileges on all tables in the public schema
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO drfadul;

-- Grant all privileges on all sequences in the public schema
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO drfadul;

-- Grant all privileges on all functions in the public schema
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO drfadul;

-- Optional: Grant all privileges on the public schema itself
GRANT ALL PRIVILEGES ON SCHEMA public TO drfadul;