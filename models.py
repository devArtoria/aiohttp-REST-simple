from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

DB_URI = 'sqlite:///stuff.db'

Session = sessionmaker(autocommit=True, autoflush=True, bind=create_engine(DB_URI))
session = scoped_session(Session)
Base = declarative_base()

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    body = Column(String(300))
    created_at = Column(DateTime(50))
    created_by = Column(String(50))

    def __init__(self, title, body, created_at ,created_by):
        self.title = title
        self.body = body
        self.created_at = created_at
        self.created_by = created_by

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        to_serialize = ['id', 'title', 'body', 'created_at', 'created_by']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        return d


if __name__ == "__main__":

    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
