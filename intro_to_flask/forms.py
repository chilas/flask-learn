from flask_wtf import Form
from wtforms.fields import TextAreaField, SubmitField, StringField,\
    PasswordField
from wtforms.validators import DataRequired, email
from models import User


class ContactForm(Form):
    name = StringField(
        "Name",
        validators=[DataRequired("Please enter your name.")]
    )
    email = StringField(
        "Email",
        validators=[DataRequired("Please enter your email address"),
                    email("Please enter a valid email address")]
    )
    subject = StringField(
        "Subject",
        validators=[DataRequired("Please enter a subject.")]
    )
    message = TextAreaField(
        "Message",
        validators=[DataRequired("Please enter a message")]
    )
    submit = SubmitField("Send")


class SignupForm(Form):
    firstname = StringField(
        "First name",
        validators=[DataRequired("Please enter your first name.")]
    )
    lastname = StringField(
        "Last name",
        validators=[DataRequired("Please enter your last name.")]
    )
    email = StringField(
        "Email",
        validators=[DataRequired("Please enter your email address."),
                    email("Please enter your email address.")]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired("Please enter a password.")]
    )
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user:
            self.email.errors.append("This email is already taken.")
        else:
            return True


class SigninForm(Form):
    email = StringField(
        "Email",
        validators=[DataRequired("Please enter your email address."),
                    email("Please enter your email address.")]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired("Please enter your password")]
    )
    submit = SubmitField("Sign In")

    def __init__(self):
        Form.__init__(self)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()

        if user and user.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Invalid email or password")
            return False