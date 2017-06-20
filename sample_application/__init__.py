__all__=['UPC','Model','Authorization']
import sample_application.UPC as UPC
import sample_application.Model as Model
from sample_application.Authorization import create_auth

import dateutil.parser
from flask import Flask, render_template,request,Response,session,flash,redirect,make_response,g
from flask_adminlte import AdminLTE
from flask_pymongo import PyMongo
from flask_login import login_user, logout_user, login_required,LoginManager
from flask_login import current_user
import datetime

import pymongo
from functools import wraps

from pymongo import MongoClient
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, (datetime.datetime, datetime.date)):
            return str(o)
        return json.JSONEncoder.default(self, o)


def create_Flask_odj(configfile):
    app = Flask(__name__)
    app.config.from_object(configfile)
    try:
        app.config.from_object('settings_local')
    except:
        pass
    print(app.config['PROJECT_FILE_NAME_SETTING'])
    lm = LoginManager()
    lm.init_app(app)
    lm.session_protection = 'strong'
    mongo = PyMongo(app)
    AdminLTE(app)
    @lm.user_loader
    def load_user(username):
            if not username:
                return None
            else:
                return Model.User_auth(username)    
    return app,lm,mongo










def create_app(configfile):
    
    app,lm ,mongo =create_Flask_odj(configfile)

    create_auth(app,mongo)

    @app.route('/')
    def start():
        return render_template('login.html')
    @app.route('/home')
    @login_required
    def home():
        User_sess=Model.User(session['User'],session['password'],mongo.db)
        return render_template('home.html',product_header=UPC.UPC_Wolmart.get_header_UPC())


    @app.route('/Data_array',methods=['POST'])
    def Data_array():
        draw=int(request.form['draw'])+1
        User_sess=Model.User(session['User'],session['password'],mongo.db)
        #print(request.form['columns['+request.form['order[0][column]']+'][data]'])
        data=User_sess.get_upc_limit_sort(int(request.form['start']),int(request.form['length']),request.form['columns['+request.form['order[0][column]']+'][data]'],
                                            (-1,1)[request.form['order[0][dir]']=='asc'])
        
        
        #for i in request.form:
        #            print((i,request.form[i]))
        #request.form['order[0][column]']
        #('order[0][column]', '0')
        #('order[0][dir]', 'desc')
        #('start', '0')
        #('length', '10')
        #('search[value]', '')
        #('search[regex]', 'false')
        return json.dumps({"draw": draw,
                             "recordsTotal": User_sess.db.UPC.count(),
                             "recordsFiltered": User_sess.db.UPC.count(),
                             "data":data}, cls=JSONEncoder)



    @app.route('/Add_upc',methods=['POST'])
    @login_required
    def Add_upc():
         User_sess=Model.User(session['User'],session['password'],mongo.db)
         User_sess.set_upc(request.form['upc'])
         if (User_sess.set_upc(request.form['upc'])!=1):
            flash("Wrong upc!", category='error')
         return redirect("/home")

    @app.route('/Del_upc',methods=['POST'])
    @login_required
    def Del_upc():
         User_sess=Model.User(session['User'],session['password'],mongo.db)
         User_sess.del_upc(request.form['upc_del'])
  
         return redirect("/home")

    @app.route('/Add_file_csv',methods=['POST'])
    @login_required
    def Add_file_csv():
         User_sess=Model.User(session['User'],session['password'],mongo.db)

         print(User_sess.set_csv(request.files['fileToUpload'].read()))
         return redirect("/home")



    @app.route('/Add_key',methods=['POST'])
    @login_required
    def Add_key():
        User_sess=Model.User(session['User'],session['password'],mongo.db)
        key = request.form['key']
        User_sess.set_key(key)
        return redirect("/home")


    @app.route('/download_example')
    def download_example():
        csv = """"upc",\n"035000521019",\n"10001137891",\n"784672839266",\n"887276181981",\n"190341996824", """
        response = make_response(csv)
        response.headers["Content-Disposition"] = "attachment; filename=example.csv"
        return response
    @app.route('/download')
    @login_required
    def download():
        User_sess=Model.User(session['User'],session['password'],mongo.db)
        csv = User_sess.get_csv()
        # We need to modify the response, so the first thing we 
        # need to do is create a response out of the CSV string
        response = make_response(csv)
        # This is the key: Set the right header for the response
        # to be downloaded, instead of just printed on the browser
        response.headers["Content-Disposition"] = "attachment; filename=database.csv"
        return response
    @app.route('/Settings',methods=['GET'])
    @login_required
    def Settings():
        User_sess=Model.User(session['User'],session['password'],mongo.db)
        key=User_sess.Key_Wolmart()
        return render_template('Settings.html',key=key)


    return app

if __name__ == '__main__':
    create_app().run(debug=True)
