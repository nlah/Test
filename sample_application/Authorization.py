import sample_application.UPC as UPC
import sample_application.Model as Model
import dateutil.parser
from flask import Flask, render_template,request,Response,session,flash,redirect,make_response
from flask_adminlte import AdminLTE
from flask_pymongo import PyMongo
from flask_login import login_user, logout_user, login_required,LoginManager
from flask_login import current_user
import pymongo
from functools import wraps
from pymongo import MongoClient
def create_auth(app,mongo):
    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/out')
    def out():
        session['User']=None
        session['password']=None
        logout_user()
        return render_template('login.html')

    @app.route('/login',methods=['POST'])
    def login_post():
        try:
            name=request.form['yourname']
            password=request.form['password']
            User_sess=Model.User(name,password,mongo.db)
            session['User']=request.form['yourname']
            session['password']=request.form['password']
            login_user(Model.User_auth(User_sess.username))
            flash("Logged in successfully!", category='success')
            return redirect("/home")
        except AttributeError:
            flash("Wrong username or password!", category='error')
            return render_template('login.html')
   
    @app.route('/login_test')
    def login_test():
        if session['session.User']==None:
            return render_template('login.html')
        else:
            return render_template('login.html')

    @app.route('/registration',methods=['GET'])
    def registration():
        return render_template('registration.html')

    @app.route('/registration',methods=['POST'])
    def registration_post():
        Model.User_generate(request.form['yourname'],request.form['password'],request.form['password_test'],mongo.db)
        return render_template('login.html')
