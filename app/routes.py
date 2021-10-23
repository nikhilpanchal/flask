from flask import render_template, flash, redirect
from flask.helpers import url_for
from app import app
from app.forms import LoginForm

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Returns false when the browser sends a GET request to retrieve the form
        # When submitted as a POST, will run all the validators associated with the fields
        # on the data submitted, and if they pass will come here
        # validators are registered in the LoginForm class
        flash('Login request for user {}, remember_me {}'.format(
            form.username.data, form.remember_me.data
        ))
        return redirect(url_for('index'))

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