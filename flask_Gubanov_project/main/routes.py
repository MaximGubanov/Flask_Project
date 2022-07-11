from flask import render_template, Blueprint
from flask_Gubanov_project.models import User, Post


main = Blueprint('main', __name__)


@main.route("/", methods=['GET'])
@main.route("/home", methods=['GET'])
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).limit(5)
    users = User.query.limit(5).all()
    return render_template('home.html', title='Главня', posts=posts, users=users)
