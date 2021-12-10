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
    # TESTS
    #------------------------------------------------------------------------------------

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 200) # Check that status code is 200
        self.assertEqual(data['success'], True) # Check that the success of the body is true
        self.assertTrue(data['categories']) # Check that there are categories in the list

    def test_404_sent_requesting_beyond_valid_page(self):  # Test that 404 is sent if we request beyond a valid page
        res = self.client().get()



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()