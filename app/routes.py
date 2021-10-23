from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form, title='Login')

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Nikhil'}
    posts = [
        {
            'author': {'username': 'Erica'},
            'body': 'Beautiful day in Jersey City!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'Avengers was awesome!'
        }
    ]

    """
    The render_template() function invokes the Jinja2 template engine that comes bundled with the 
    Flask framework. Jinja2 substitutes {{ ... }} blocks with the corresponding values, given by 
    the arguments provided in the render_template() call.
    """
    return render_template('index.html', title="Flask Tutorial", user=user, posts=posts)