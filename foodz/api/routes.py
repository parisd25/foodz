from flask import Blueprint, request, jsonify
from werkzeug.wrappers import response
from foodz.helpers import token_required
from foodz.models import db,User,Foodz,foodz_schema,foodzs_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def get_data(current_user_token):
    return {'some' : 'value'}

#Create foodz ENDPOINT
@api.route('/foodzs', methods = ['POST'])
@token_required
def create_foodz(current_user_token):
    name = request.json['name']
    ingredients = request.json['ingredients']
    servings = request.json['servings']
    instructions = request.json['instructions']
    user_token = current_user_token.token

    foodz = Foodz(name,ingredients, servings, instructions, user_token)
    db.session.add(foodz)
    db.session.commit()

    response = foodz_schema.dump(foodz)
    return jsonify(response)

# RETRIEVE ALL foodzs ENDPOINT
@api.route('/foodzs', methods = ['GET'])
@token_required
def get_foodzs(current_user_token):
    owner = current_user_token.token
    foodzs = Foodz.query.filter_by(user_token = owner).all()
    response = foodzs_schema.dump(foodzs)
    return jsonify(response)

# retrieve one foodz endpoint
@api.route('/foodzs/<id>', methods = ['GET'])
@token_required
def get_foodz(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        foodz = Foodz.query.get(id)
        response = foodz_schema.dump(foodz)
        return jsonify(response)
    else:
        return jsonify({'message' : 'Valid Token Required'}),401

# UPDATE foodz ENDPOINT

@api.route('/foodzs/<id>', methods = ['POST','PUT'])
@token_required
def update_foodz(current_user_token, id):
    foodz = Foodz.query.get(id) # Get foodz Instance

    foodz.name = request.json['name']
    foodz.ingredients = request.json['ingredients']
    foodz.servings = request.json['servings']
    foodz.instructions = request.json['instructions']
    foodz.user_token = current_user_token.token

    db.session.commit()
    response = foodz_schema.dump(foodz)
    return jsonify(response)


# DELETE ENDPOINT

@api.route('/foodzs/<id>', methods = ['DELETE'])
@token_required
def delete_foodz(current_user_token, id):
    foodz = Foodz.query.get(id)
    db.session.delete(foodz)
    db.session.commit()

    response = foodz_schema.dump(foodz)
    return jsonify(response)