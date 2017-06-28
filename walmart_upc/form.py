
"""
"A universal convention supplies all of maintainability,
clarity, consistency, and a foundation for good programming habits too.
What it doesn't do is insist that you follow it against your will. That's Python!"
—Tim Peters on comp.lang.python, 2001-06-16
"""
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms import validators
from walmart_upc.objects_behevior import User

class LoginForm(FlaskForm):

    username = TextField(u'Username', validators=[validators.required()])

    password = PasswordField(u'Password', validators=[validators.optional()])


    def validate(self):
        """ Validate user form """

        check_validate = super(LoginForm, self).validate()
        if not check_validate:
            return False
        user = User.get_user(self.username.data, self.password.data)
        if not user:
            self.username.errors.append('Invalid username or password')
            return False
        return True

class RegistrationForm(FlaskForm):
    """ Registration user form """

    username = TextField(u'Username', validators=[validators.required()])

    password = PasswordField(u'Password', validators=[validators.optional()])

    password_again = PasswordField(u'Рassword again', validators=[validators.optional()])

    def validate(self):
        """ Validate user form """

        check_validate = super(RegistrationForm, self).validate()
        if self.password.data != self.password_again.data:
            self.username.errors.append('passwords are not equal')
            return False
        if not check_validate:
            return False

        user = User.generate(self.username.data, self.password.data)
        if not user:
            self.username.errors.append('Username is exist')
            return False
        return True
