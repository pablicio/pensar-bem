from psycopg2.pool import ThreadedConnectionPool

from config import DATABASE_URL

pool = ThreadedConnectionPool(minconn=2, maxconn=10, dsn=DATABASE_URL)
