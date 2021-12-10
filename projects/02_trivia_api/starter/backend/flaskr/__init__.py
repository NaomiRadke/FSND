import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Method for paginating questions
def paginate_questions(request, all_questions):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in all_questions]
  current_questions = questions[start:end]
  return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  # set up CORS, allow '*' for origins
  CORS(app)
  cors = CORS(app, resources={r"*": {"origins": "*"}})
  
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

 
# ----------------------------------------------------------------------------------------
# ENDPOINTS
# ----------------------------------------------------------------------------------------

  # Endpoint to GET all available categories
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    categoryTypes = {category.id: category.type for category in categories}

    return jsonify({
      'success':True,
      'categories': categoryTypes
    })

# Endpoint to GET questions, including pagination (every 10 questions)
  @app.route('/questions')
  def get_paginated_questions():
    all_questions = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, all_questions)
    categories = Category.query.all()
    formatted_categories = {
      category.id: category.type for category in categories}

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(Question.query.all()),
      'current_category': None,
      'categories': formatted_categories
    })

 
# Endpoint to DELETE a question of a given id
  '''
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      question = Question.query.filter_by(id=id).one_or_none() # get the question from db
      if question is None: abort(404) # if question id does not exist: abort 404
      question.delete()

      return jsonify({
        'success': True,
        'deleted': id
      })
    except:
      abort(422)
    

# Endpoint to POST a new question
  '''
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions/add', methods=['POST'])
  def add_question():
    # get the data from the user input
    data = request.get_json()
    new_question = data.get('question')
    new_answer = data.get('answer')
    new_category = data.get('category')
    new_difficulty = data.get('difficulty')

    # add it to the database
    try:
      question = Question(
        question=new_question,
        answer=new_answer,
        category=new_category,
        difficulty=new_difficulty
      )
      question.insert()

      return jsonify({
        'success': True,
        'created': question.id,
        'total_questions': len(Question.query.all())
      })
    except:
      abort(422)


    

# Endpoint for searching the questions for a search term
  '''

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    search_term = request.form.get('search_term', '')
    try:
      result = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
      current_questions = paginate_questions(request, result)
      
      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(Question.query.all()),
        'current_category': None
      })
    except: 
      abort(422)


# Endpoint for getting questions based on a category
  '''
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:cat_id>/questions')
  def questions_by_category(cat_id):

    try:
      result = Question.query.filter(Question.category == str(cat_id)).all()
      current_questions = paginate_questions(request, result)

      if result is None: 
        abort(404)

      return jsonify(
        {
          'success': True,
          'questions': result,
          'total_questions': len(Question.query.all())
        }
      )
    except:
      abort(422)

# Endpoint to get questions to play the quiz based on category and previous question parameters

  '''
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    data = request.get_json()
    previous_question = data.get('previous_questions', [])
    quiz_category = data.get('quiz_category', None)

    try:
      if quiz_category:
        if quiz_category['id'] == 0:
          quiz = Question.query.all()
        else:
          quiz = Question.query.filter_by(category=quiz_category['id']).all()
        if not quiz:
          return abort(422)
        selected = []
        for question in quiz:
          if question.id not in previous_questions:
            selected.append(question.format())
          if len(selected) != 0:
            result = random.choice(selected)
            return jsonify({
              'question': result
            })
          else:
            return jsonify({
              'question': False
            })
    except:
        abort(404)



# Define error handlers
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad request'
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Resource not found'
    }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'Method not allowed'
    }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'Unprocessable'
    }), 422

  @app.errorhandler(500)
  def server_error(error):
      return jsonify({
          "success": False,
          "error": 500,
          "message": "Server Error"
      }), 500

  

  
  return app

    