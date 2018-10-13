from sqlalchemy import Column, Integer, String, DateTime
from models import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    body = Column(String(300))
    created_at = Column(DateTime(50))
    created_by = Column(String(50))

    def __init__(self, title, body, created_at, created_by):
        self.title = title
        self.body = body
        self.created_at = created_at
        self.created_by = created_by

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        to_serialize = ['id', 'title', 'body', 'created_at', 'created_by']
        data = {}
        for attr_name in to_serialize:
            data[attr_name] = getattr(self, attr_name)
        return data
