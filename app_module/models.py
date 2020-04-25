from flask_sqlalchemy import SQLAlchemy
from app_module import db ,login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    date_of_birth = db.Column(db.Date , nullable = False)
    classname = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(120), unique = True)

    def __repr__(self):
        return f"User('{self.name}', '{self.date_of_birth}', '{self.email}', '{self.classname}')"       #Các trường sẽ được show.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"          #chỉ show username và email thôi