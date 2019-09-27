import secrets,os,requests
from app import create_app
from flask import render_template,redirect,url_for
from . import auth
from flask import flash,request
from .forms import RegistrationForm,LoginForm,UpdateAccountForm 
from .. models import User, Post
from .. import db,bcrypt
from flask_login import login_user,logout_user,login_required,current_user
from . import auth
from .. import mail
from app import create_app

app = create_app('development')


@auth.route('/register',methods = ["GET","POST"])
def register():
    if current_user.is_authenticated:
        return  redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, pass_secure = hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created! You are now able to login', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', registration_form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.pass_secure, form.password.data):
            login_user(user, form.remember.data)
            next_page = request.args.get('next')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/logout')
@login_required
def logout():     
    logout_user()
    return redirect (url_for('main.index'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex +f_ext
    picture_path = os.path.join(app.root_path, 'static/images',picture_fn)
    form_picture.save(picture_path)

    return picture_fn

@auth.route('/account', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image_file.data:
            image_file = save_picture(form.image_file.data)
            current_user.image_file = image_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account details have been updated!', 'success')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username   
        form.email.data = current_user.email 
        form. contact.data = current_user. contact
        form.bio.data = current_user.bio              
    image_file = url_for('static', filename = 'images/' + current_user.image_file)
    return render_template('profile.html', title='Account', image_file = image_file, form=form)  
