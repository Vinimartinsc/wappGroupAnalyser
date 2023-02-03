from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime

Base = declarative_base()


class Messages(Base):
    '''The whatsapp message database model.'''

    __tablename__ = 'messages'

    id = Column("id", Integer, primary_key=True)
    at_datetime = Column("at_datetime", DateTime(), nullable=False)
    author = Column("author", String(), nullable=False)
    raw = Column("raw", String(), nullable=False)
    type = Column("type", String(), nullable=False)
    content = Column("content", String(), nullable=False)
