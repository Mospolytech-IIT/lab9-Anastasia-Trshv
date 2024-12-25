from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

class Base(DeclarativeBase): pass

class User(Base):

    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    posts = relationship('Post', back_populates='author')

class Post(Base):

    __tablename__ = "Posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("Users.id"))

    author = relationship('User', back_populates='posts')
