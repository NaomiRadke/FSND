
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
        #self.token_cd = os.environ['TOKEN_CD'] # Authorization token for casting director
        #self.token_e = os.environ['TOKEN_E'] # Authorization token for executive
        self.token_cd = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVtd2J5S05DRklKMThIWXJZaDNyYSJ9.eyJpc3MiOiJodHRwczovL2Rldi11MWJ2YXp0OS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkZGE5NzRhZTI5YjMwMDc2NDU3MTNkIiwiYXVkIjoiY2Fwc3RvbmVfaW1hZ2UiLCJpYXQiOjE2NDIxNTI4MDMsImV4cCI6MTY0MjIyNDgwMywiYXpwIjoibElQVU1YVjBhaHNGNWFRcmdZeGk2NThCZTNGbUZKZnAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.mahdtZg_JKfv-HA9tB_uhy4XY0Z3khf-6Stai9Yz_-UYnSL8FlS1IjqRH3M_YXEZzfl6AT_X4mKQqZ8FTBg0nSl3nagRPiuMyEJaJlr2dficPGV0BfETSoc38AXVos2DkgGJeUlxC7w-rJ0zRQeIz1wVh8wAmaqHlygwkK0P9ZsY04ODSpNxPOD1C86wKnHLUF5QLpluzPJWmRTiZQMWgkwwcZC1rl5-oO4DF14zm9yyulJkIJSKGkjbun_MPN5iy4qYFbE6L54qgXlkzwjQAZ-5jLlwo_G4wadA9RbGkWSk09Ksa270SLongs5xrmeAYOHulX-auCDUzIDs6eRgwg'    
        self.token_e = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVtd2J5S05DRklKMThIWXJZaDNyYSJ9.eyJpc3MiOiJodHRwczovL2Rldi11MWJ2YXp0OS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkZGE4ODNkMTg4ZDgwMDZlYTQ5YTg1IiwiYXVkIjoiY2Fwc3RvbmVfaW1hZ2UiLCJpYXQiOjE2NDIxNTI2OTksImV4cCI6MTY0MjIyNDY5OSwiYXpwIjoibElQVU1YVjBhaHNGNWFRcmdZeGk2NThCZTNGbUZKZnAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.6VN7peaY8x6gNM29DviaxlBu4S0XSHZ71pap87EE7dNoZP8PYjpmeV4xcSuYrTHpElI7ftBDb19Q2UAlCot3UoWbrBo9kDY-6H2wGA3gPrj5SfMmBwy1uTdu-Xajoq0kWwlmg5nuM2GDQskW_crdArWa1wmdZJd8ynbdCrFC16vlAQUXI5VuKJSiInZNam963SvQklW11TE8WgxMw-d1XcZTokz5UmLMB0ns7ngNnzO1sGNEeHtUbfXiohvAcn2TgODJAUStRApfs9UT4dbQpjH5A9XVdTOxFowlGiBQn9MHtsin3c9fg5ce4OQt6MrXNk7IGNYqtPrDcXc_ag_Lxg'
        setup_db(self.app, self.database_path)

        self.cd_headers = {
            "Authorization": self.token_cd
        }
        self.e_headers = {
            "Authorization": self.token_e
        }

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
        res = self.client().delete('actors/8', headers={
            'Authorization': 'Bearer {}'.format(self.token_cd)}) # Delete actor with actor_id=8
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
        res = self.client().post('/actors/8', json = {'name': None}, headers={
            "Authorization": "Bearer {}".format(self.token_cd)})
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
        res = self.client().patch('/actors/1000', json = {'name': 'Miss New'}, headers={
            "Authorization": "Bearer {}".format(self.token_e)})
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