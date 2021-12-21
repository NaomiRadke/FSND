import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, get_token_auth_header, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# Initialize a database
db_drop_and_create_all()

# ROUTES

# GET drinks (public)
@app.route('/drinks')
def get_drinks():
    try:
        drinks = [drink.short() for drink in Drink.query.order_by(Drink.id).all()]

        return jsonify({
            'success' : True,
            'drinks' : drinks    
        })
    except:
        abort(422)


# GET drink details (only for baristas)
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail():

    try:
        drinks = [drink.long() for drink in Drink.query.order_by(Drink.id).all()]
        if len(drinks) == 0:
            abort(404)
        return jsonify({
            'success' : True,
            'drinks' : drinks
        }), 200
    except AuthError:
        abort(422)

# POST new drinks (only managers)
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(jwt):
    body = request.get_json()
    drink_title = body.get('title', None)
    drink_recipe = body.get('recipe', None)
    try:
        drink = Drink(title=drink_title, recipe=drink_recipe)
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200
    except AuthError:
        abort(422)


# PATCH (edit) existing drinks (only managers)
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(jwt, id):
    body = request.get_json()
    drink_title = body.get('title')
    drink_recipe = body.get('recipe')

    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if len(drink) == 0:
            abort(404)

        drink.title = drink_title
        drink.recipe = drink_recipe
        drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200

    except AuthError:
        abort(422)


# DELETE drink (only managers)
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if len(drink) == 0:
            abort(404)

        drink.delete()
        return jsonify({
            'success': True,
            'delete': id
        })
    except AuthError:
        abort(422)


# Error Handling

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(AuthError)
def handle_auth_error(error):
    response = jsonify(ex.error)
    response.status_code = error.status_code
    return response

