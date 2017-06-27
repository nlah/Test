"""
"A universal convention supplies all of maintainability,
clarity, consistency, and a foundation for good programming habits too.
What it doesn't do is insist that you follow it against your will. That's Python!"
—Tim Peters on comp.lang.python, 2001-06-16
"""
from flask import render_template, request, \
 redirect, Blueprint, flash
from flask_login import login_user, logout_user
import walmart_upc.objects_behevior as model

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    """ Return login.html """

    return render_template('login.html')

@auth.route('/out')
def out():
    """ Logouting user and go to login.html """

    logout_user()
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    """ User verification """

    try:
        user = model.User.get_user(request.form['yourname'], request.form['password'])
        login_user(user)
        flash("Logged in successfully!", category='success')
        return redirect("/home")
    except (AttributeError, model.UserModel.DoesNotExist):
        flash("Wrong username or password!", category='error')
        return render_template('login.html')

@auth.route('/registration', methods=['GET'])
def registration():
    """ Return registration.html """

    return render_template('registration.html')

@auth.route('/registration', methods=['POST'])
def registration_post():
    """ Registration new user """
    
    try:
        model.UserGenerate(request.form['yourname'], request.form['password'],\
         request.form['password_test'])
    except Exception as err:
        flash(err.args, category='error')
    return render_template('login.html')
