from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Email
# from flaskblog.models import Contact


class ContactForm (FlaskForm):
    name = StringField('Name', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email_id = StringField('Email', validators=[DataRequired(), Email()])
    heading = StringField('Heading', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post query')
