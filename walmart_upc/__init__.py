"""
"A universal convention supplies all of maintainability,
clarity, consistency, and a foundation for good programming habits too.
What it doesn't do is insist that you follow it against your will. That's Python!"
—Tim Peters on comp.lang.python, 2001-06-16
"""
from flask import Flask
from flask_adminlte import AdminLTE
from flask_login import LoginManager
from walmart_upc.controllers import authorization, main
import walmart_upc.model as Model


def create_flask_odj():
    """ Configures flask object """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('settings')
    app.config.from_pyfile('log_settings.py')
    lm = LoginManager()
    lm.init_app(app)
    lm.session_protection = 'strong'
    lm.login_view = "auth.login"
    Model.db.init_app(app)
    AdminLTE(app)
    @lm.user_loader
    def load_user(email):

        try:
            return Model.UserModel.objects.get(email=email)
        except:
            return None
    return app


def create_app():
    """ Return flask object """

    app = create_flask_odj()
    app.register_blueprint(authorization.auth)
    app.register_blueprint(main.main)
    return app

if __name__ == '__main__':
    create_app().run(debug=True)
