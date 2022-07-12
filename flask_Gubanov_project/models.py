from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

from flask_Gubanov_project import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except Exception as err:
            print(err)
            return None
        return User.query.get(user_id)

    @staticmethod
    def get_top_users(limit=5):
        users = User.query.filter(User.posts).all()
        return users


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_likes = db.Column(db.Integer, nullable=True, default=0)
    likes = db.relationship('Like', backref='like')
    post_image = db.Column(db.String(20), nullable=False, default='post_default_img.png')
    comments = db.relationship('Comment', backref='post')

    @staticmethod
    def counter_likes(post_id):
        all_likes = Like.query.filter(Like.post_id == post_id).all()
        post = Post.query.get(post_id)
        post.total_likes = len(all_likes)
        db.session.add(post)
        db.session.commit()

    @staticmethod
    def get_top_posts_by_likes(limit=1):
        list_order = Post.query.order_by(Post.total_likes.desc()).limit(limit)
        return list_order

    @staticmethod
    def get_last_post(limit=1):
        last_post = Post.query.order_by(Post.date_posted.desc()).limit(limit)
        return last_post

    def total_comments(self):
        c = Comment.query.filter(Comment.post_id == self.id).all()
        return len(c)

    def __repr__(self):
        return f"Запись('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_commented = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    username = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)

    @staticmethod
    def get_comments_order_by_desc(post_id):
        c = Comment.query.order_by(Comment.date_commented.desc()).filter(Comment.post_id == post_id).all()
        return c
