from flask import render_template, request, Blueprint
from flaskblog.models import Post
from flaskblog import db


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)

    # this is to find all distinct values of categories available in the db
    dis_cats = []
    for dis_cat in db.session.query(Post.category).distinct():
        dis_cats.append(dis_cat.category)
    
    return render_template('home.html', posts=posts, dis_cats=dis_cats)


@main.route("/about")
def about():
    # this is to find all distinct values of categories available in the db
    dis_cats = []
    for dis_cat in db.session.query(Post.category).distinct():
        dis_cats.append(dis_cat.category)
    return render_template('about.html', title='About', dis_cats=dis_cats)
