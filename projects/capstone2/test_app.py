import unittest
from enum import Enum
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import Actors, Movies, setup_db
import os


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        
        # self.token_cd = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVtd2J5S05DRklKMThIWXJZaDNyYSJ9.eyJpc3MiOiJodHRwczovL2Rldi11MWJ2YXp0OS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkZGE5NzRhZTI5YjMwMDc2NDU3MTNkIiwiYXVkIjoiY2Fwc3RvbmVfaW1hZ2UiLCJpYXQiOjE2NDQwMDA0NDksImV4cCI6MTY0NDA3MjQ0OSwiYXpwIjoibElQVU1YVjBhaHNGNWFRcmdZeGk2NThCZTNGbUZKZnAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.AD2Z6SQ1DnvKbNSAAj7GC_etoQHSL012uRJdYGdnAIvAk0_NNjgsMOS__XAzMIwbrSC0lBoRB0gN_WNURVQrlLt0YEp0E2vNR_TX6yhll86AwT5-MESkQnnQFlFBlZavNjN9j1YR3VPioT7R0XWgGDeMyeBZ6l2Y4vCkWbVHGNe6ZcscmgZppIcuHnVgLwVShL49LAmXKhh3iEbm7agKThB2HjgFAlyZ5hjJ5Ugxuv6xCS-4zxVlc96HXuARsCNq_5doxsvi6sOmd_J9_BWV4__btMisOST30xaCtde7pkPKCfvu32paN712fvsL3_cKK3fIydNE0-2nhGnXZ8drew'
        # self.token_e = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVtd2J5S05DRklKMThIWXJZaDNyYSJ9.eyJpc3MiOiJodHRwczovL2Rldi11MWJ2YXp0OS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkZGE4ODNkMTg4ZDgwMDZlYTQ5YTg1IiwiYXVkIjoiY2Fwc3RvbmVfaW1hZ2UiLCJpYXQiOjE2NDQwMDA3MTYsImV4cCI6MTY0NDA3MjcxNiwiYXpwIjoibElQVU1YVjBhaHNGNWFRcmdZeGk2NThCZTNGbUZKZnAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.tvYuNe8qNVeiGI4xV1C1ZPz0LUmwSHYJslqvDkFuCgt1nwfaOV9KDVJK0cfisbNhS7jXABOPeuwCeCsANGF6CdArEdW-U75Nve3wCF_wh16axHZzC1Oyd1BYPUE2avpwuIdlNAyFLQcHkeXNC4_ZtljmyNHr3CvjW3GAKfHsQn4wa1D4KraQd1L06kR2bmX2S3in5JoXCs18TW_r35X_1whECJ5aq17g2ZFknhyCZDoMxJ7cCJrKHWQgleAKjvP40-buiMnT5JugLqgVYoDreD9cKI0NPICnhHJ3klMcprdCwvijh6PDiyQw3ZXXZg5KqVscCrSkcu0nkUaNBwhVJg"
        self.tokend_cd = os.environ['TOKEN_CD']
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

    # ACTORS
    #----------------------------------------
    # Get all available actors 
    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) # Check that status code is 200
        self.assertEqual(data['success'], True) # Check that the success of the body is true
        self.assertTrue(data['actors']) # Check that there are actors in the list

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

    # Get actor by id
    def get_actory_by_id(self):
        res = self.client().get('/actors/6')      
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

    # Patch an actor with id 'actor_id'
    def test_patch_actor(self):
        res = self.client().patch('/actors/2', json={'name': 'Updated', 'age': 10, 'gender': 'f'}, headers={'Authorization': self.token_e})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    def test_422_no_data(self):
        res = self.client().patch('/actors/3', headers={'Authorization': self.token_e})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    # Delete actor with id 'actor_id'
    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers={'Authorization': format(self.token_cd)}) # Delete actor with actor_id=8
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 1).one_or_none() # Check that the actor is no longer in the database
        
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



    


    # MOVIES
    #----------------------------------------

    # Get all available movies 
    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) # Check that status code is 200
        self.assertEqual(data['success'], True) # Check that the success of the body is true
        self.assertTrue(data['movies']) 

    # Post a new movie
    def test_post_movie(self):
        res = self.client().post('/movies', json={'title': 'Brave New World', 'release_date': '1980-05-04 00:00:00'}, headers={'Authorization': self.token_e})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_movies'])

    def test_422_movie_unprocessable(self):
        res = self.client().post('/movies', json={'title': 'no movie'}, headers={'Authorization': self.token_e})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Get movies by id
    def get_movie_by_id(self):
        res = self.client().get('/movies/4')      
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) # Check that status code is 200
        self.assertEqual(data['success'], True) # Check that the success of the body is true
        self.assertTrue(data['movie'])

    def test_404_movie_does_not_exist(self):

        res = self.client().get('/movies/13563')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found') 

    # Patch a movie with id 'movie_id'
    def test_patch_movie(self):
        res = self.client().patch('/movies/2', json={'title': 'This is an update!', 'release_date': '1980-05-04 00:00:00'}, headers={'Authorization': self.token_e})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    def test_422_no_data(self):
        res = self.client().patch('/movies/3', headers={'Authorization': self.token_cd})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    # Delete movie with id 'movie_id'
    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers={'Authorization': format(self.token_e)}) 
        data = json.loads(res.data)

        movie = Movies.query.filter(Movies.id == 1).one_or_none() # Check that the movie is no longer in the database
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(movie, None) # Check that movie no longer exists

    def test_401_unauthorized_movie_delete(self):

        res = self.client().delete('/movies/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'authentication error')


        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()