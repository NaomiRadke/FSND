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
        
        self.token_cd = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVtd2J5S05DRklKMThIWXJZaDNyYSJ9.eyJpc3MiOiJodHRwczovL2Rldi11MWJ2YXp0OS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkZGE5NzRhZTI5YjMwMDc2NDU3MTNkIiwiYXVkIjoiY2Fwc3RvbmVfaW1hZ2UiLCJpYXQiOjE2NDMxODgzMDEsImV4cCI6MTY0MzI2MDMwMSwiYXpwIjoibElQVU1YVjBhaHNGNWFRcmdZeGk2NThCZTNGbUZKZnAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.3562o-NuycOAX9WznfP7zp9TGK5SLS_fqNSZO8FW9nXOFDDMDjH_EYNFH5M1q8xiYezmdq8PuRbYYZJx64INvSHwvqyx1AFs0YpKd1HRaDhQozYtVWAyWCsJYb-QeZAfs3nsAsKvKUAvybB-QmP-Lw2Y4N3SnYUwgEXLr7LuT0sJR1qV50CRw2j6kfK5xt1mDIK1Wv46ngvvKhvdUDaFIIt53JmoVhDdCRHzt3J2rJx8-LurVdtQfO8BWU3UQmG8rMahFCD0-4nZOcUifFkLz35tYbtoCzxaj4O9MOnHeuk0XwZqAgKIJg8vn9a6f4n9NpONldeNWeh19albj6zBjQ'
        self.token_e = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVtd2J5S05DRklKMThIWXJZaDNyYSJ9.eyJpc3MiOiJodHRwczovL2Rldi11MWJ2YXp0OS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkZGE4ODNkMTg4ZDgwMDZlYTQ5YTg1IiwiYXVkIjoiY2Fwc3RvbmVfaW1hZ2UiLCJpYXQiOjE2NDMxODgxOTUsImV4cCI6MTY0MzI2MDE5NSwiYXpwIjoibElQVU1YVjBhaHNGNWFRcmdZeGk2NThCZTNGbUZKZnAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.XGqmkwfu0UpBSciN7AZRGLk46V4v_fWvJJDOVLpINzF7I3ZekDsFlvioYWSGXgCjLcDk1pIfSNjT_YMvrZONGKnbKjT5LbOVQBsGEyuap5CJbNM4uVDrQ8ik5tUmVG2sHWSY4G7jHThv6Jw8mkE8tB9DFVFb8s4Auev8Q9QaoBZy0gob9Oug3i2f5dBD9cCfGHfJj7AcIomattZ2L79A0256hcgTnMwTAMibj8U_p7oyWESCQ2b3WYaSjHEPR5EtnEs_P4W3GotJOtwYwrwzWy3OziaaHIGJfBmg7tUFNWtIOJDHbYjReHfxUyXP7_dk24R_HS9aMsvOoXEptxU9ow"
        
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
        res = self.client().post('/actors', json={'age': 9, 'gender': 'f'}, headers={'Authorization': self.token_cd})
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
        res = self.client().delete('/movies/8', headers={'Authorization': format(self.token_e)}) 
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 8).one_or_none() # Check that the movie is no longer in the database
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(movie, None) # Check that movie no longer exists

    def test_404_movie_does_not_exist(self):

        res = self.client().delete('/movies/10000', headers={'Authorization': self.token_e})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Post a new movie
    def test_post_movie(self):
        res = self.client().post('/movies', json={'title': 'Brave New World', 'release_date': '1980-05-04 00:00:00'}, headers={'Authorization': self.token_e})
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
        res = self.client().patch('/movies/9', json={'title': 'This is new!', 'release_date': '1980-05-04 00:00:00'}, headers={'Authorization': self.token_e})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    def test_422_no_data(self):
        res = self.client().patch('/movies/9', json={'name': 'nobody'}, headers={'Authorization': self.token_e})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()