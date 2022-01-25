import unittest
from enum import Enum
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import Actors, Movies, setup_db


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        
        self.token_cd = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVtd2J5S05DRklKMThIWXJZaDNyYSJ9.eyJpc3MiOiJodHRwczovL2Rldi11MWJ2YXp0OS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkZGE5NzRhZTI5YjMwMDc2NDU3MTNkIiwiYXVkIjoiY2Fwc3RvbmVfaW1hZ2UiLCJpYXQiOjE2NDMxMDc1NjEsImV4cCI6MTY0MzE3OTU2MSwiYXpwIjoibElQVU1YVjBhaHNGNWFRcmdZeGk2NThCZTNGbUZKZnAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.0maau4yrv9TTfu1eFPq2q5ljpo3chyQH_kN_ZX5AQQo59_fasgnlZK1X6f9KZ28BRbFjiwdgcn5NYKTYIhJwOoqD96WjfxGaZvNtgGinAWRfGtfJRn2rI72LRQnkUoy57LW8nIWjwTFXUL5g3ZKSCfT0fH0JPUfbMPMiYfgwPb4_0-RAy3n4VO8htlDk9Yn_FzYofX5l_XgEBt8x6Iuzoxn7VMZ5gMX0jn0dcGhNNYI-G4hdAgSqAP9-oPQDoaqAFYCXnlIfKDWY5sHWELGCYF5hv5ZwcGGveL2qSFEbsoB1zsYGJV1wZ-B1Epr-DDsLs4j_4m6MBAgNPp0SOLuLPQ'
        self.token_e = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVtd2J5S05DRklKMThIWXJZaDNyYSJ9.eyJpc3MiOiJodHRwczovL2Rldi11MWJ2YXp0OS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkZGE4ODNkMTg4ZDgwMDZlYTQ5YTg1IiwiYXVkIjoiY2Fwc3RvbmVfaW1hZ2UiLCJpYXQiOjE2NDMxMDc0NzYsImV4cCI6MTY0MzE3OTQ3NiwiYXpwIjoibElQVU1YVjBhaHNGNWFRcmdZeGk2NThCZTNGbUZKZnAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.Gu0l-BmAEruBftqfdblcX7bi10KokSmMDsDcPyFeBTDiGZzTLU-4lNxqnO_JiaUk3JzxMiQy0BEe8a5uidjPvJBT_-68RfX7HaAK2a4yYhRqyJyCaMu7vKKKQx-zD04jgP1YbxWXCr25kvXoCh5gEGHv-njSpRCkDwdPXxbxMBTRop0xo2ssjHlKL_94hTiwYN9KfwK5ju_E2Oa5TiH7H0-yrPQbe9vrswwXaDlXSvyUjP_FCwfcQZyJo3dg0x2hsPoT-Y71zvjuFb_uHlq56ls7W6rdLdgrN9-W9p4QDPMIdghVl31mIacc8kXkjI6X3ty2bq37D5wnUcAnPwGpLw"
        
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

    # ACTORS
    #----------------------------------------
    # Get all available actors 
    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) # Check that status code is 200
        self.assertEqual(data['success'], True) # Check that the success of the body is true
        self.assertTrue(data['actors']) # Check that there are actors in the list

    # Get actor by id
    def get_actory_by_id(self):
        res = self.client().get('/actors/7')      
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) # Check that status code is 200
        self.assertEqual(data['success'], True) # Check that the success of the body is true
        self.assertTrue(data['actor'])

    def test_404_actor_does_not_exist(self):

        res = self.client().get('/actors/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found') 


    # Delete actor with id 'actor_id'
    def test_delete_actor(self):
        res = self.client().delete('/actors/10', headers={'Authorization': format(self.token_cd)}) # Delete actor with actor_id=8
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 10).one_or_none() # Check that the actor is no longer in the database
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(actor, None) # Check that actor no longer exists

    def test_404_actor_does_not_exist(self):

        res = self.client().delete('/actors/10000', headers={'Authorization': self.token_cd})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Post a new actor
    def test_post_actor(self):
        res = self.client().post('/actors', json={'name': 'Hello Kitty', 'age': 10, 'gender': 'f'}, headers={'Authorization': self.token_cd})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_actors'])

    def test_422_actor_unprocessable(self):
        res = self.client().post('/actors', json={'name': 'Hello Kitty', 'age': True, 'gender': 'f'}, headers={'Authorization': self.token_cd})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Patch an actor with id 'actor_id'
    def test_patch_actor(self):
        res = self.client().patch('/actors/9', json={'name': 'Hello Kitty', 'age': 10, 'gender': 'f'}, headers={'Authorization': self.token_e})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    def test_422_no_data(self):
        res = self.client().patch('/actors/9', headers={'Authorization': self.token_e})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    # MOVIES
    #----------------------------------------

    # Get all available movies 
    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) # Check that status code is 200
        self.assertEqual(data['success'], True) # Check that the success of the body is true
        self.assertTrue(data['movies']) 

    # Get movies by id
    def get_movie_by_id(self):
        res = self.client().get('/movies/7')      
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) # Check that status code is 200
        self.assertEqual(data['success'], True) # Check that the success of the body is true
        self.assertTrue(data['movie'])

    def test_404_movie_does_not_exist(self):

        res = self.client().get('/movies/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found') 


    # Delete movie with id 'movie_id'
    def test_delete_movie(self):
        res = self.client().delete('/movies/10', headers={'Authorization': format(self.token_e)}) 
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 7).one_or_none() # Check that the movie is no longer in the database
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(movie, None) # Check that actor no longer exists

    def test_404_movie_does_not_exist(self):

        res = self.client().delete('/movies/10000', headers={'Authorization': self.token_e})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Post a new movie
    def test_post_movie(self):
        res = self.client().post('/movies', json={'title': 'Brave New World', 'release_date': '1980-05-04 00:00:00'}, headers={'Authorization': self.token_cd})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_movies'])

    def test_422_movie_unprocessable(self):
        res = self.client().post('/movies', json={'name': 'no movie'}, headers={'Authorization': self.token_e})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Patch a movie with id 'movie_id'
    def test_patch_movie(self):
        res = self.client().patch('/movies/8', json={'title': 'This is new!', 'release_date': '1980-05-04 00:00:00'}, headers={'Authorization': self.token_e})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    def test_422_no_data(self):
        res = self.client().patch('/movies/9', headers={'Authorization': self.token_e})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()