from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    username = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)

    def __repr__(self):
        return f"<Like> id:{self.id}, post_id:{self.post_id}, username:{self.username}"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"Пользователь('{self.username}','{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_likes = db.Column(db.Integer, nullable=True, default=0)
    likes = db.relationship('Like', backref='like')
    post_image = db.Column(db.String(20), nullable=False, default='post_default_img.png')

    def __repr__(self):
        return f"Запись('{self.title}', '{self.date_posted}')"


if __name__ == '__main__':
    db.drop_all()
    db.create_all()

