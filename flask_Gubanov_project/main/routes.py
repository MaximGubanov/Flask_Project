from flask import render_template, Blueprint
from flask_Gubanov_project.models import User, Post


main = Blueprint('main', __name__)


@main.route("/", methods=['GET'])
@main.route("/home", methods=['GET'])
def home():

    last_posts = Post.get_last_post(limit=10)
    top_posts = Post.get_top_posts_by_likes(limit=5)
    top_users = User.get_top_users(limit=5)

    return render_template('home.html',
                           title='Главня',
                           top_posts=top_posts,
                           last_posts=last_posts,
                           top_users=top_users
                           )
