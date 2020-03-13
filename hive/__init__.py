import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_login import current_user,LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '81f50e907d84d4370595c16fc8bef7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['FLASK_ADMIN_SWATCH'] = 'Flatly'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bestabaidullahbutt@gmail.com'
app.config['MAIL_PASSWORD'] = 'ansans267@'
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
# ENV='dev'
# if ENV=='dev':
#     app.debug=True
#     # app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:butt@localhost/school'
# else:
#     app.debug=False
#     app.config['SQLALCHEMY_DATABASE_URI']='postgres://gnrwyxnwchsdzd:0b87c666c4c2546d1fb91a616bb08b2c212c3f0668bdff07225db7ffe7e642b6@ec2-174-129-255-57.compute-1.amazonaws.com:5432/d2ia3uvabgi19o'
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
