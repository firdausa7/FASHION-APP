from flask import render_template, redirect,url_for
from . import auth
from .forms import RegistrationForm,LoginForm,UpdateAccountForm
from .. import db
from app.models import User

@auth.route('/register',methods = ['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, pass_secure=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template("auth/register.html",registration_form=form)
