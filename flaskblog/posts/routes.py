from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm
from flaskblog.posts.utils import save_picture


posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if (form.picture.data):
            picture_file = save_picture(form.picture.data)
        else:
            picture_file='default1.jpg'
        post = Post(title=form.title.data, content=form.content.data, author=current_user, image_file=picture_file, category=form.category.data)

        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')

        return redirect(url_for('main.home'))
    dis_cats = []
    for dis_cat in db.session.query(Post.category).distinct():
        dis_cats.append(dis_cat.category)
    return render_template('create_post.html', title='New Post', form=form, dis_cats=dis_cats, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    dis_cats = []
    for dis_cat in db.session.query(Post.category).distinct():
        dis_cats.append(dis_cat.category)

    return render_template('post.html', title=post.title, image_file=post.image_file, post=post, dis_cats=dis_cats)


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
        # post.category= form.content.category
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category.data  = post.category
    dis_cats = []
    for dis_cat in db.session.query(Post.category).distinct():
        dis_cats.append(dis_cat.category)

    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post', dis_cats=dis_cats)

# route to delete posts
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


# route to view posts by category
@posts.route("/post/<string:category>")
def cat_post(category):
    page = request.args.get('page', 1, type=int)

    posts = Post.query.filter_by(category=category).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    dis_cats = []
    for dis_cat in db.session.query(Post.category).distinct():
        dis_cats.append(dis_cat.category)

    return render_template('cat_post.html', posts=posts, category=category, dis_cats=dis_cats)
