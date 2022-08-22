from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:tnpdnem12@localhost/fastapi'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)
Base = declarative_base()


# Dependency
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()