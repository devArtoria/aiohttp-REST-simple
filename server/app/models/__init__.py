from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os

basedir = os.path.abspath(os.path.dirname(__file__))

DB_URI = 'mysql+pymysql://root:asdfqwer@localhost:3306/posts'

session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=True,
                                      bind=create_engine(DB_URI)))
Base = declarative_base()

if __name__ == "__main__":
    engine = create_engine(DB_URI, echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
