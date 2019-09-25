import os
from flask import render_template,url_for,flash,request,redirect
from . import auth
import secrets
from .. import db,bcrypt
from flask_login import login_user,logout_user,login_required,current_user
from .forms import LoginForm,RegistrationForm
from . import auth
from .. import mail
from ..models import User


@auth.route('/register',methods = ["GET","POST"])
def register():
    if current_user.is_authenticated:
        return  redirect(url_for('main.home'))
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
            flash('Loggin Unsuccessful. Please check email and password', 'danger')    
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/logout')
@login_required
def logout():     
    logout_user()
    return redirect (url_for('main.index'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join( 'app/static/profile_pics', picture_fn)

    output_size = (125, 125)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    

    return picture_fn
