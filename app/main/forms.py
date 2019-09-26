from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from ..models import User, Post, Comment
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError




class PostForm(FlaskForm):
    
    design_name= StringField('Title', validators = [DataRequired()])
    description = TextAreaField('Content', validators = [DataRequired()])
    design_image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png','jpeg'])])

    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    text= TextAreaField('Leave a comments', validators=[DataRequired()])

    submit = SubmitField('Submit')
