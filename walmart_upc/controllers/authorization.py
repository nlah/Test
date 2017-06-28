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
from walmart_upc.form import LoginForm, RegistrationForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    """ Return login.html if you don't authorized """

    form = LoginForm()
    if form.validate_on_submit():
        user = model.User.get_user(form.username.data, form.password.data)
        login_user(user)
        flash("Logged in successfully.", "success")
        return redirect("/home")
    return render_template("login.html", form=form)


@auth.route('/out')
def out():
    """ Logouting user and go to login.html """

    logout_user()
    return redirect("/login")

@auth.route('/registration', methods=['POST', 'GET'])
def registration():
    """ Return registration.html if you don't authorized """
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect("/login")
    return render_template("registration.html", form=form)
