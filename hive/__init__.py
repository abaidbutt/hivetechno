import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_login import current_user,LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = '81f50e907d84d4370595c16fc8bef7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hivetec2_hivetec:hivetecsite@https://hivetechnologies.org:2083/hivetec2_site'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hivetec2_hivetec:hivetecsite@hivetechnologies.org:2083/hivetec2_site'
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hivetechnologies8@gmail.com'
app.config['MAIL_PASSWORD'] = '123@Hive'
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
# ENV='dev'
# if ENV=='dev':
#     app.debug=True
#     # app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:butt@localhost/school'
# else:
#     app.debug=False
    # app.config['SQLALCHEMY_DATABASE_URI']='postgres://hivetec2_hivetecsite:hivetecsite@hivetechnologies.org:2083/hivetec2_hivetec2site'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id=='0'

login_manager=LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
# db.drop_all()
# db.create_all()
admin = Admin(app, name='Hivetech', template_mode='bootstrap3', index_view=MyAdminIndexView())

from hive import routes
