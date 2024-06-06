from sqlalchemy import Column, CHAR
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class BaseModel(Base):
    __abstract__ = True

    id = Column(CHAR(36), primary_key=True, default=generate_uuid, nullable=False)
