from flask import render_template
from . import main


@main.route('/')
def index():

    return render_template("index.html")
@main.route('/about')
def about_us():
    """ View root page function that returns index page """

    # category = Category.get_categories()

    return render_template('about.html')
