import secrets
import requests
import os

from flask import render_template, url_for, flash, redirect, request
from . import main
from .forms import CommentForm, PostForm
from ..models import Post, User
from app import create_app
from .. import db
from flask_login import login_required, current_user


app = create_app('development')


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/about')
def about_us():
    """ View root page function that returns index page """

    return render_template('about.html')


@main.route('/designers')
def designs():
    """ View root page function that returns index page """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('designers.html', posts=posts)


def save_design_image(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    form_picture.save(picture_path)

    return picture_fn


@main.route('/post', methods=['POST', 'GET'])
@login_required
def new_design_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.design_image.data:
            picture_file = save_design_image(form.design_image.data)
            design_image = picture_file

        post = Post(design_image=design_image, design_name=form.design_name.data,
                    description=form.description.data, designer=current_user)
        db.session.add(post)
        db.session.commit()

        flash('Posted successfully!', 'success')
        return redirect(url_for('main.index'))

    return render_template('create_design_post.html', title=Post.design_name, post_form=form)
