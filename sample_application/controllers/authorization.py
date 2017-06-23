"""
"A universal convention supplies all of maintainability,
clarity, consistency, and a foundation for good programming habits too.
What it doesn't do is insist that you follow it against your will. That's Python!"
—Tim Peters on comp.lang.python, 2001-06-16
"""
from flask import render_template, request, \
 redirect, Blueprint, flash
from flask_login import login_user, logout_user
import sample_application.objects_behevior as Model
Auth = Blueprint('Auth', __name__)
@Auth.route('/login')
def login():
    return render_template('login.html')

@Auth.route('/out')
def out():
    logout_user()
    return render_template('login.html')
@Auth.route('/login', methods=['POST'])
def login_post():
    try:
        user = Model.User.get_user(request.form['yourname'], request.form['password'])
        login_user(user)
        flash("Logged in successfully!", category='success')
        return redirect("/home")
    except AttributeError:
        flash("Wrong username or password!", category='error')
        return render_template('login.html')

@Auth.route('/registration', methods=['GET'])
def registration():
    return render_template('registration.html')

@Auth.route('/registration', methods=['POST'])
def registration_post():
    try:
        Model.User_generate(request.form['yourname'], request.form['password'],\
         request.form['password_test'])
    except Exception as err:
        flash(err.args, category='error')
    return render_template('login.html')
