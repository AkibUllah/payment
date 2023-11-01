from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

dbcon = 'sqlite:///fastapidb.sqlite3'

engine = create_engine(dbcon)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
