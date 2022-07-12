from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from wtforms import SubmitField

from flask_Gubanov_project import db
from flask_Gubanov_project.models import Post, Like, Comment
from flask_Gubanov_project.posts.forms import PostForm, CommentForm
from flask_Gubanov_project.users.utils import save_picture

posts = Blueprint('posts', __name__)


@posts.route("/allpost")
@login_required
def allpost():
    page = request.args.get('page', 1, type=int)
    all_posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('allpost.html', posts=all_posts)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        if form.picture.data:
            picture_file = save_picture(form.picture.data, path_save='static/post_images')
            post.post_image = picture_file
        db.session.add(post)
        db.session.commit()
        flash('Ваш пост создан!', 'success')
        return redirect(url_for('posts.allpost'))
    return render_template('create_post.html', title='Новый пост', form=form, legend='Новый пост')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.get_comments_order_by_desc(post_id)
    try:
        liked = Like.query.filter(Like.post_id == post_id, Like.username == current_user.username).first()
        return render_template('post.html', title=post.title, post=post, liked=liked, comments=comments)
    except AttributeError:
        return render_template('post.html', title=post.title, post=post, comments=comments)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if form.picture.data:
            picture_file = save_picture(form.picture.data, path_save='static/post_images')
            post.post_image = picture_file
        db.session.commit()
        flash('Ваш пост обновлен!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Обновление поста', form=form, legend='Обновление поста')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Ваш пост был удален!', 'success')
    return redirect(url_for('posts.allpost'))


@posts.route("/post/<int:post_id>/like", methods=['POST'])
@login_required
def like_post(post_id):
    try:
        like = Like.query.filter(Like.post_id == post_id, Like.username == current_user.username).first()
        if like:
            flash('Вы уже ставили лайк к этой записи!', 'success')
            return redirect(url_for('posts.post', post_id=post_id))
        else:
            new_like = Like(post_id=post_id, username=current_user.username)
            db.session.add(new_like)
            db.session.commit()
            Post.counter_likes(post_id)
            return redirect(url_for('posts.post', post_id=post_id))
    except Exception as err:
        print(err)
        return redirect(url_for('posts.allpost'))


@posts.route("/post/<int:post_id>/add-comment", methods=['POST'])
@login_required
def add_comment(post_id):
    try:
        data = request.form['comment']
        limit_symbol = 1000
        if isinstance(data, str) and 0 < len(data) < limit_symbol:
            comment = Comment(username=current_user.username, post_id=post_id, content=request.form['comment'])
            db.session.add(comment)
            db.session.commit()
    except Exception as err:
        print(err)
        return redirect(url_for('posts.post', post_id=post_id))
    return redirect(url_for('posts.post', post_id=post_id))


@posts.route("/post/<int:comment_id>/del-comment/<int:post_id>/", methods=['POST'])
@login_required
def delete_comment(post_id, comment_id):
    try:
        c = Comment.query.get(comment_id)
        c.is_deleted = True
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('posts.post', post_id=post_id))
    except Exception as err:
        print(err)
    return redirect(url_for('posts.post', post_id=post_id))
