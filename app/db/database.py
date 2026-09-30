import os
import ssl
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

# ✅ Env-driven DB settings (no hardcoded credentials)
DB_USER = os.environ["DB_USER"]
DB_PASSWORD_RAW = os.environ["DB_PASSWORD"]
DB_PASSWORD = quote_plus(DB_PASSWORD_RAW)

DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

# ✅ Optional: allow overriding entire URL directly (useful in Docker/K8s)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Enable SSL for remote connections (Cloud SQL requirement)
# 'cert_reqs': ssl.CERT_NONE skips server certificate verification (same as DBeaver)
connect_args = {}
if "localhost" not in DB_HOST and "127.0.0.1" not in DB_HOST:
    connect_args = {
        "ssl": {
            "check_hostname": False,
            "cert_reqs": ssl.CERT_NONE
        }
    }

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()