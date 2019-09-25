import secrets, requests,os
from flask import render_template
from . import main
from  .forms import CommentForm, PostForm
from ..models import Post, User
from app import create_app
from .. import db



app = create_app('development')



@main.route('/')
def index():

    return render_template("index.html")
@main.route('/about')
def about_us():
    """ View root page function that returns index page """

    # category = Category.get_categories()

    return render_template('about.html')
@main.route('/designers')
def designs():
    """ View root page function that returns index page """

    # category = Category.get_categories()

    return render_template('designers.html')



def save_design_image(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex +f_ext
    picture_path = os.path.join(app.root_path, 'static/images',picture_fn)
    form_picture.save(picture_path)

    return picture_fn




@main.route('/post', methods = ['POST', 'GET'])
# @login_required
def new_design_post():
    form = PostForm()
    if form.validate_on_submit():
        
        picture_file = save_design_image(form.design_image.data)
        
        new_post = Post(design_name=form.design_name.data, description = form.description.data, design_image = picture_file)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('main.index'))
    return render_template('create_design_post.html',title = Post.design_name, post_form = form)

