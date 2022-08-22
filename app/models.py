from tokenize import String
from turtle import title
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Post(Base):
    #table name
    __tablename__ = 'posts'

    #define columns
    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, default = True)
    




