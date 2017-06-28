"""
"A universal convention supplies all of maintainability,
clarity, consistency, and a foundation for good programming habits too.
What it doesn't do is insist that you follow it against your will. That's Python!"
—Tim Peters on comp.lang.python, 2001-06-16
"""
import json
import datetime
from bson import ObjectId
from flask import Blueprint, render_template, request,\
 flash, redirect, make_response
from flask_login import  login_required, current_user
import walmart_upc.objects_behevior as model

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
@login_required
def home():
    """ Start page for login user """

    return render_template('home.html', product_header=model.UpcWalmart.get_header_upc())

@main.route('/data-array', methods=['POST'])
@login_required
def data_array():
    """ Data for datateble """

    class JSONEncoder(json.JSONEncoder):
        """ Fix error """

        def default(self, o):
            """



            Args:

              o:



            Returns:



            """

            if isinstance(o, ObjectId):
                return str(o)
            if isinstance(o, (datetime.datetime, datetime.date)):
                return str(o)
            return json.JSONEncoder.default(self, o)

    draw = int(request.form['draw'], base=0) + 1
    user = model.User(current_user)
    data = user.get_upc_limit_sort(int(request.form['start']), int(request.form['length']),\
      request.form['columns[' + request.form['order[0][column]'] + '][data]'],\
      (-1, 1)[request.form['order[0][dir]'] == 'asc'])

    data = json.dumps({"draw": draw,
                       "recordsTotal": user.count_upc(),
                       "recordsFiltered": user.count_upc(),
                       "data":data}, cls=JSONEncoder)
    return data

@main.route('/add-upc', methods=['POST'])
@login_required
def add_upc():
    """ Add walmart object """

    user = model.User(current_user)
    user.set_upc(request.form['upc'])
    if user.set_upc(request.form['upc']) != 1:
        flash("Wrong upc or key!", category='error')
    return redirect("/home")

@main.route('/del-upc', methods=['POST'])
@login_required
def del_upc():
    """ Delete walmart object  """

    user = model.User(current_user)
    user.del_upc(request.form['upc_del'])
    return redirect("/home")

@main.route('/add-file-csv', methods=['POST'])
@login_required
def add_file_csv():
    """ Add upc from csv  """

    user = model.User(current_user)
    err_key = user.set_csv(request.files['fileToUpload'].read())
    if len(err_key) > 0:
        flash("Wrong upc "+str(len(err_key)), category='error')
    return redirect("/home")

@main.route('/add-key', methods=['POST'])
@login_required
def add_key():
    """ Add key walmart """

    user = model.User(current_user)
    key = request.form['key']
    user.set_key(key)
    return redirect("/home")

@main.route('/download-example')
def download_example():
    """ Return csv example """

    csv = """"upc",n"035000521019",n"10001137891","""

    response = make_response(csv)
    response.headers["Content-Disposition"] = "attachment; filename=example.csv"
    return response

@main.route('/download')
@login_required
def download():
    """ Walmart data in csv format  """

    user = model.User(current_user)
    csv = user.get_csv()
    response = make_response(csv)
    response.headers["Content-Disposition"] = "attachment; filename=database.csv"
    return response

@main.route('/Settings', methods=['GET'])
@login_required
def Settings():
    """ Return Settings.html and key user"""

    user = model.User(current_user)
    key = user.key_walmart()
    return render_template('Settings.html', key=key)

