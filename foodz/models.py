from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from sqlalchemy.orm import backref

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import Secrets module (Givenby Python)
import secrets

#Imports for Login Manager
from flask_login import UserMixin, login_manager

#Imports for Flask Login
from flask_login import LoginManager

# Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow



db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String(150), primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email =  db.Column(db.String(150), nullable = False)
    password =  db.Column(db.String, nullable = True, default = '')
    g_auth_verify =  db.Column(db.Boolean, default = False)
    token =  db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    foodz = db.relationship('Foodz', backref = 'owner', lazy = True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database.' 

class Foodz(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    ingredients = db.Column(db.String(200), nullable = True)
    servings = db.Column(db.Numeric(precision=10, scale=2))
    instructions = db.Column(db.String(150), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, ingredients, servings, instructions, user_token, id=''):
        self.id = self.set_id()
        self.name = name
        self.ingredients = ingredients
        self.servings = servings
        self.instructions = instructions
        self.user_token = user_token

    def __repr__(self):
        return f'The following Recipe has been added: {self.name}'

    def set_id(self):
        return secrets.token_urlsafe()

# Creation of API Schema via the Marshmallow Object
class FoodzSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'ingredients', 'servings', 'instructions']

foodz_schema = FoodzSchema()

foodzs_schema = FoodzSchema(many=True)