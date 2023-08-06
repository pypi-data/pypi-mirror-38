from sqlalchemy import create_engine
from sqlalchemy import Column, Table
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base


MODEL_BASE = declarative_base()


class BaseInterface(object):
    def __init__(self, engine: Engine):
        self.engine = engine
        self.session_maker = sessionmaker(bind=self.engine)
        self.session = self.session_maker()

    @classmethod
    def from_db_uri(cls, uri: str):
        engine = create_engine(uri)
        return cls(engine)

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def read_one(self, *args, **kwargs):
        raise NotImplementedError

    def read_all(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


def initiate_database(uri):
    engine = create_engine(uri)
    MODEL_BASE.metadata.create_all(engine)
    return engine
