from flask import render_template, request, Blueprint, flash
from flaskblog.models import Post, Contact
from flaskblog import db
from flaskblog.main.forms import ContactForm


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


@main.route("/about", methods=['GET', 'POST'])
def about():
    form = ContactForm()
    if form.validate_on_submit():
        temp = Contact(name=form.name.data, email_id = form.email_id.data, heading=form.heading.data, content=form.content.data)

        db.session.add(temp)
        db.session.commit()
        flash('Your query is posted. We will contact you shortly', 'success')

    # this is to find all distinct values of categories available in the db
    dis_cats = []
    for dis_cat in db.session.query(Post.category).distinct():
        dis_cats.append(dis_cat.category)
    return render_template('about.html', title='About', dis_cats=dis_cats, form=form)
