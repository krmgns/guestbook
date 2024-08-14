from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from __util import parse_dotenv

# Please change the creds in .env file.
options = parse_dotenv()
DB_HOST = options["DB_HOST"]
DB_NAME = options["DB_NAME"]
DB_USER = options["DB_USER"]
DB_PASS = options["DB_PASS"]

# SQLAlchemy engine.
# @see https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-sqlalchemy-engine
engine = create_engine(
    "postgresql://%s:%s@%s/%s" % (DB_USER, DB_PASS, DB_HOST, DB_NAME),
    # echo=True # For debugging only (env option can be used here).
)

# Database session class.
# @see https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-sessionlocal-class
SessionLocal = sessionmaker(
    bind=engine, autocommit=False, autoflush=False
)

# Base ORM model.
# @see https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-base-class
Base = declarative_base()

# Used as dependency.
def connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
