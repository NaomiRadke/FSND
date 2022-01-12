import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actors, Movies
from auth import requires_auth, AuthError



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  # set up CORS, allow '*' for origins
  CORS(app)
  cors = CORS(app, resources={r"*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
      response.headers.add(
          'Access-Control-Allow-Headers',
          'Content-Type,Authorization'
      )
      response.headers.add(
          'Access-Control-Allow-Methods',
          'GET,POST,PATCH,DELETE,OPTIONS'
      )
      return response


  # Endpoints
  # -----------------------------------------------------------------

  # Welcome page
  @app.route('/')
  def get_welcome():
    return "Hello to the casting agency"

  # GET actors
  @app.route('/actors')
  def get_actors():
    all_actors = Actors.query.order_by(Actors.id).all()
    format_actors = [actor.format() for actor in all_actors]
    

    if len(all_actors) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'actors': format_actors
    })

  # DELETE actors
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(jwt, actor_id):
    try:
      actor = Actors.query.filter(Actors.id==actor_id).one_or_none()
      if actor_id is None: 
        abort(404)
      actor.delete()

      return jsonify({
        'success': True,
        'deleted': actor_id
      })
    except AuthError:
      abort(422)

  # POST actors
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def add_actor(jwt):
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
  def update_actor(jwt, actor_id):
    
    body = request.get_json()

    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)

    if new_name is None and new_age is None and new_gender is None:
      abort(422)

    try:
      actor = Actors.query.filter(Actors.id==actor_id).one_or_none()
      actor_formatted = actor.format()
      
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
    all_movies = Movies.query.order_by(Movies.id).all()
    format_actors = [actor.format() for actor in all_movies]
  

    if len(all_movies) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'movies': format_actors
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

      return jsonify({
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
  def auth_error(error):
      return jsonify({
          "success": False,
          "error": AuthError,
          "message": "authentication error"
      }), 401


  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)