
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import *



class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        self.token_cd = os.environ['TOKEN_CD']
        self.token_e = os.environ['TOKEN_E']
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        
    
    def tearDown(self):
        """Executed after each test"""
        pass

    #------------------------------------------------------------------------------------
    # TESTS FOR ENDPOINTS
    #------------------------------------------------------------------------------------

    # Get all available actors (paginated)
    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) # Check that status code is 200
        self.assertEqual(data['success'], True) # Check that the success of the body is true
        self.assertTrue(data['actors']) # Check that there are actors in the list


    # Delete actor with id 'actor_id'
    def test_delete_actor(self):
        res = self.client().delete('actor/2', headers={'Authorization': 'Bearer {}'.format(
                                       self.token_cd)
                                   }) # Delete actor with actor_id=2
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 2).one_or_none() # Check that the question is no longer in the database
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success', True])
        self.assertTrue(data['deleted'])
        self.assertEqual(actor, None) # Check that actor no longer exists

    def test_404_actor_does_not_exist(self):
        res = self.client().delete('/actors/10000', headers={
            "Authorization": "Bearer {}".format(self.token_cd)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Post new actor
    def test_create_new_actor(self):
        res = self.client().post('/actors', json={'name': 'Hello Kitty', 'age': 10, 'gender': 'f'}, headers={
            "Authorization": "Bearer {}".format(self.token_cd)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_actors'])

    def test_422_if_actor_creation_not_allowed(self):
        res = self.client().post('/actors/2', json = {'name': None})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message', 'unprocessable'])

    
    # Update (patch) actor with id 'actor_id'
    def test_update_actor(self):
        res = self.client().patch('/actors/2', json={'name': 'Hello Kitty', 'age':10, 'gender':'m'}, headers={
            "Authorization": "Bearer {}".format(self.token_e)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    def test_422_if_patch_not_allowed(self):
        res = self.client().patch('/actors/1000', json = {'name': 'Miss New'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message', 'unprocessable'])


    # Get all availabe movies (paginated)

    # Delete movie with id 'movie_id'

    # Post new movie

    # Update (patch) movie with id 'movie_id'



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()