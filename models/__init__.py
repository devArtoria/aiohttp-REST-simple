from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DB_URI = 'sqlite:///stuff.db'

session = scoped_session(sessionmaker(autocommit=True,
                                      autoflush=True,
                                      bind=create_engine(DB_URI)))
Base = declarative_base()

if __name__ == "__main__":

    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
