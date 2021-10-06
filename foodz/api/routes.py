from flask import Blueprint, request, jsonify
from werkzeug.wrappers import response
from foodz.helpers import token_required
from foodz.models import db,User,Foodz,foodz_schema,foodzs_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def get_data(current_user_token):
    return {'some' : 'value'}
