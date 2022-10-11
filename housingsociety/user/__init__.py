from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import re,os
from flask_mail import Mail

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/housingsociety'
db = SQLAlchemy(app)

app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] ='djangopro3031@gmail.com'
app.config['MAIL_PASSWORD'] = 'django@3031'

mail=Mail(app)

# import a blueprint that we will create
from housingsociety.admin.views import register_blueprint
from housingsociety.user.views import userlogin_blueprint
from housingsociety.user.maintaince import maintaince_blueprint
# register our blueprints with the application
app.register_blueprint(register_blueprint)
app.register_blueprint(userlogin_blueprint)
app.register_blueprint(maintaince_blueprint)