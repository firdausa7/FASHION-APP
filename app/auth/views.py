import secrets,os,requests
from app import create_app
from flask import render_template,redirect,url_for
from . import auth
from flask import flash,request
from .forms import RegistrationForm,LoginForm,UpdateAccountForm 
from .. models import User, Post
from .. import db,bcrypt
from flask_login import login_user,logout_user,login_required,current_user



@auth.route('/register',methods = ["GET","POST"])
def register():
    # if current_user.is_authenticated:
    #     return  redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created! You are now able to login', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', registration_form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
    quote_data = requests.get('http://quotes.stormconsultancy.co.uk/random.json' ).json()
    quote_content= quote_data.get('quote')
    quote_author= quote_data.get('author')
    
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', title='Login', form=form,quote=quote_content, author=quote_author)

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
