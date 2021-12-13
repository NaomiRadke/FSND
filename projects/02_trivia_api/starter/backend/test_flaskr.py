import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    #------------------------------------------------------------------------------------
    # TESTS FOR ENDPOINTS
    #------------------------------------------------------------------------------------

    # Get all available categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 200) # Check that status code is 200
        self.assertEqual(data['success'], True) # Check that the success of the body is true
        self.assertTrue(data['categories']) # Check that there are categories in the list

    # Get questions including pagination
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) # Check that status code is 200
        self.assertEqual(data['success'], True) # Check that the success of the body is true
        self.assertTrue(data['questions']) # Check that there are questions in the list
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(data['categories'])

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000', json={'category': 0}) # Check for a unrealistic page number
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')


    # Delete a question of a given id
    def test_delete_question(self):
        res = self.client().delete('questions/10')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 10).one_or_none()  # Check that the question is no longer in the database

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(question, None) # Check that question no longer exists

    def test_404_question_does_not_exist(self):
        res = self.client().delete('/questions/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')


    # Post a new question
    def test_create_new_question(self):
        res = self.client().post('/questions', json={'new_question':'Is this new?'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])

    def test_405_if_question_creation_not_allowed(self):
        res = self.client(). post('/questions/405', json = {'new_question':'Is this new?'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')



    # Searching questions for a search term
    def test_searching_questions(self):
        res = self.client().post('/questions/search', json = {'search_term':''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

        # No "fail" test required, since we have not defined search term rules


    # Getting questions based on category 
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/3/questions') # Checking for category id 1
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_404_category_does_not_exist(self):
        res = self.client().get('/categories/10000/questions') 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')




    # Getting questions based on category + previous question parameters
    def test_post_quizzes(self):
        parameters= {
            "previous_questions":[2],
            "quiz_category":{'id': 2} 
        }
        res = self.client().post('/quizzes', json = parameters)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])


    def test_404_invalid_parameters(self):
        parameters= {
            "previous_questions":[100000],
            "quiz_category":{'id': 2000} 
        }
        res = self.client().post('/quizzes', json = parameters)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')









# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()