import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
from auth import requires_auth, AuthError


# Methods for paginating movies and actors
ENTRIES_PER_PAGE = 10 # Set maximum # of entries per page

# Paginating actors
def paginate_actors(request, result):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * ENTRIES_PER_PAGE
  end = start + ENTRIES_PER_PAGE
  
  actors = [actor.format() for actor in result]
  current_actors = actors[start:end]

  return current_actors

# Paginating movies
def paginate_movies(request, result):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * ENTRIES_PER_PAGE
  end = start + ENTRIES_PER_PAGE
  
  movies = [movie.format() for movie in result]
  current_movies = movies[start:end]

  return current_movies



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  # Endpoints
  # -----------------------------------------------------------------

  # Welcome page
  @app.route('/')
  def get_welcome():
    return "Hello to the casting agency"

  # GET actors
  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors():
    result = Actors.query.order_by(Actors.id).all()
    current_actors = paginate_actors(request, result)

    if len(current_actors) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'actors': current_actors
    })

  # DELETE actors
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  def delete_actor(payload, actor_id):
    try:
      actor = Actors.query.filter(Actors.id==actor_id).one_or_none()
      if actor_id is None: 
        abort(404)
      actor.delete()

      return json({
        'success': True,
        'deleted': actor_id
      })
    except AuthError:
      abort(422)

  # POST actors
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def add_actor(payload):
    body = request.get_json() # Get the data from the entry fields

    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)

    try:
      actor = Actors(
        name = new_name,
        age = new_age,
        gender = new_gender
      )
      actor.insert()

      return jsonify({
        'success': True,
        'created': actor.id,
        'total_actors': len(Actors.query.all())
      }), 200
    except AuthError:
      abort(422)

  # PATCH actors
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(payload, actor_id):
    body = request.get_json()

    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)

    if new_name is None and new_age is None and new_gender is None:
      abort(422)

    try:
      actor = Actors.query.filter(Actors.id==actor_id).one_or_none()
      
      actor.name = new_name
      actor.age = new_age
      actor.gender = new_gender

      actor.update()

      return jsonify({
        'success': True,
        'updated': actor_id
      }), 200
    except AuthError:
      abort(422)



  # GET movies
  @app.route('/movies')
  def get_movies():
    result = Movies.query.order_by(Movies.id).all()
    current_movies = paginate_movies(request, result)

    if len(current_movies) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'movies': current_movies
    })

  # DELETE movies
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, movie_id):
    try:
      movie = Movies.query.filter(Movies.id==movie_id).one_or_none()
      if movie_id is None: 
        abort(404)
      movie.delete()

      return json({
        'success': True,
        'deleted': movie_id
      }), 200
    except:
      abort(422)

  # POST movie
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def add_movie(payload):
    body = request.get_json() # Get the data from the entry fields

    new_title = body.get('title', None)
    new_release_date = body.get('release_date', None)

    try:
      movie = Movies(
        title = new_title,
        release_date = new_release_date
      )
      movie.insert()

      return jsonify({
        'success': True,
        'created': movie.id,
        'total_movies': len(Movies.query.all())
      }), 200
    except AuthError:
      abort(422)

  # PATCH movies
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(payload, movie_id):
    body = request.get_json()

    new_title = body.get('title', None)
    new_release_date = body.get('release_date', None)

    if new_title is None and new_release_date is None:
      abort(422)

    try:
      movie = Movies.query.filter(Movies.id==movie_id).one_or_none()
      
      movie.title = new_title
      movie.age = new_release_date

      movie.update()

      return jsonify({
        'success': True,
        'updated': movie_id
      }), 200
    except AuthError:
      abort(422)

  # Error handlers
  # -----------------------------------------------------------------
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
  def server_error(error):
      return jsonify({
          "success": False,
          "error": error.code,
          "message": error.description
      }), error.status_code


  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)