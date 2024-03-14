from sqlalchemy import Column, Integer, String, Text, ForeignKey
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from extensions import db


class Base(db.Model):
    __abstract__ = True


class User(UserMixin, Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

    # ***************Parent Relationship*************#
    posts = relationship('BlogPost', back_populates='author')
    comments = relationship('Comment', back_populates='comment_author')


class BlogPost(Base):
    __tablename__ = "blog_posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(250), unique=True, nullable=False)
    subtitle = Column(String(250), nullable=False)
    date = Column(String(250), nullable=False)
    body = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    author = relationship('User', back_populates='posts')
    img_url = Column(String(250), nullable=False)

    # ***************Parent Relationship*************#
    comments = relationship("Comment", back_populates='parent_post')


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    comment_author = relationship('User', back_populates='comments')

    # ***************Child Relationship*************#
    post_id = Column(Integer, ForeignKey('blog_posts.id'))
    parent_post = relationship("BlogPost", back_populates='comments')
    text = Column(Text, nullable=False)