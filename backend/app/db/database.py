# backend/app/db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# MySQL connection URL format
# mysql+pymysql://user:password@host:port/dbname
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,       # auto reconnect if connection drops
    pool_size=10,             # number of connections in pool
    max_overflow=20           # extra connections allowed beyond pool_size
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# ```

# ---

# **Your config file for env variables:**
# ```
# backend/app/core/config.py