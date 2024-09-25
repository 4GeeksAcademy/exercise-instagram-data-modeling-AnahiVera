import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Table, func
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er


Base = declarative_base()

likes_posts = Table(
    "likes_posts",
    Base.metadata,
    Column("posts_id", Integer, ForeignKey('posts.id'), primary_key=True, nullable=False),
    Column("users_id", Integer, ForeignKey('users.id'), primary_key=True, nullable=False)    
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    fullname = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    posts = relationship ("Post", back_populates="users")
    comment= relationship ("Comment", back_populates="users")
    liked_posts = relationship("Post", secondary=likes_posts, back_populates="likes")


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user= relationship("User", back_populates="posts")
    comment= relationship ("Comment", back_populates="posts")
    liked_posts = relationship("Post", secondary=likes_posts, back_populates="likes")

   
class Comment(Base):
     __tablename__ = 'comments'
     id = Column(Integer, primary_key=True)
     message = Column(Text, nullable=False)
     date_message = Column(DateTime, default=func.now())
     posts_id = Column(Integer, ForeignKey('posts.id'))
     users_id = Column(Integer, ForeignKey('users.id'))
     user= relationship("User", back_populates="comments")
     post= relationship("Post", back_populates="comments")





## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
