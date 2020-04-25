from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import  JWTManager


app = Flask(__name__)           #khởi tạo app.
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cmtiszogmzuimr:fc8af57bca31bf8735c2b216b7276b33aed67f2c7714c26f9ac12cb5175320ad@ec2-18-206-84-251.compute-1.amazonaws.com:5432/dfd5cetjrf47j9'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'huylinh1703'


jwt = JWTManager(app)
db = SQLAlchemy(app)            #khởi tạo db
bcrypt = Bcrypt(app)            #khởi tạo bcrypt
ma = Marshmallow(app)           #khở tạo ma
login_manager = LoginManager(app)

CORS(app)

from app_module import routes