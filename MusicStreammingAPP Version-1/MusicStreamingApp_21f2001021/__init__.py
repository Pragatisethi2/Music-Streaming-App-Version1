# from flask import Flask , render_template , url_for , redirect
# from flask_sqlalchemy import SQLAlchemy
# from application.forms import RegistrationForm , LoginForm
# from werkzeug.security import generate_password_hash, check_password_hash
# from application.models import User , Admin , UserMixin
# from flask_login import LoginManager




# db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__)
#     # __name__ is the special function which gives the name of the current local python file 
#     # This is needed so that Flask knows where to look for resources such as templates and static file
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#     app.config['SECRET_KEY']='28ef91619bab9f89d5689b25'
   
#     db.init_app(app)
#     app.app_context().push()
    
#     login_manager = LoginManager()


   
#     login_manager.login_view = "login"
#     login_manager.init_app(app)
    
    
    
#     return app

# #def create_database():



