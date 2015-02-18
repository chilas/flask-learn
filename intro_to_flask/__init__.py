from flask import Flask

# app configuration
SECRET_KEY = '0pnhGcFrESXcYrmbmJKw7c7SZZ5^C2EjOagod' \
             'AyDuuX#XSMHztSAszBN6YYfex@eKM99CzyOYd!' \
             'LN6#S$lF2y0RBfgZOH@gsLv4b'
DEBUG = True
# HOST = '0.0.0.0'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'princechilas@gmail.com'
MAIL_PASSWORD = 'thisemailisnotsecure'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:toor@localhost/development'
# SQLALCHEMY_DATABASE_URI = os.getenv('CLEARDB_DATABASE_URL')
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://bdccdab7e8dcdb:356f0a62@us-cdbr-iron-east-01.cleardb.net' \
                          '/heroku_0e6459298234bbe'
# initialize app
app = Flask(__name__)
app.config.from_object(__name__)

#flask-login setup
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'signin'
login_manager.init_app(app)

# email setup
from routes import mail
mail.init_app(app)

# db setup
from models import db
db.init_app(app)