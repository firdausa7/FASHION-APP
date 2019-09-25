from . import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True) 
    username = db.Column(db.String(255),unique=True, nullable=False)
    email = db.Column(db.String(255),unique=True, nullable=False)
    image_file = db.Column(db.String(255), nullable=False, default='default.jpg')
    pass_secure = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.String(255))
    contact = db.Column(db.Integer)
    posts = db.relationship('Post',backref='author',lazy=True)
    design_name = db.Column(db.String(100),nullable=False)
    

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    design_name = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime, nullable = False, default =datetime.utcnow)
    description  = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable = False)
    comment = db.relationship('Comment',backref='comment',lazy = 'dynamic' )

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable = False, default =datetime.utcnow)
    comment  = db.Column(db.Text,nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'), nullable = False)


