import unittest
from enum import Enum
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import Actors, Movies, setup_db

token_cd = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVtd2J5S05DRklKMThIWXJZaDNyYSJ9.eyJpc3MiOiJodHRwczovL2Rldi11MWJ2YXp0OS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkZGE5NzRhZTI5YjMwMDc2NDU3MTNkIiwiYXVkIjoiY2Fwc3RvbmVfaW1hZ2UiLCJpYXQiOjE2NDI0MTE5MzgsImV4cCI6MTY0MjQ4MzkzOCwiYXpwIjoibElQVU1YVjBhaHNGNWFRcmdZeGk2NThCZTNGbUZKZnAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.IcKYuat-G3L5K83IndHUKVuzlq_8R8ebjYOQr98MKE6LsKeqs-sOYcBPek9L9CNcqF5NTXyIYpjuzfNZhq-HBoCITNcomxFp1P2b769j1__2wi6hhiDWs21WHmgDt23hPOmp_AgtfaXazSjYOH91zwKv1GUYzTcTfkUjRAm3-C66rca-NuUuIXBeS95S3Cr8arrM6vYmw24fGZeLdKUEzklfhpogIY4qlzcq3E1Oukn_Lk07Pco1BvnEFrj5sEjOB-nZ8D-5sHnRg1ITFWEqKf_onuXFCLnZ1BdXvzZlkEDISokHyYFvbIB90J27mAS-ZyQq9vH8vqg9j9ZpjUrs-Q'   

class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        
        self.token_cd = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVtd2J5S05DRklKMThIWXJZaDNyYSJ9.eyJpc3MiOiJodHRwczovL2Rldi11MWJ2YXp0OS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkZGE5NzRhZTI5YjMwMDc2NDU3MTNkIiwiYXVkIjoiY2Fwc3RvbmVfaW1hZ2UiLCJpYXQiOjE2NDI0MTE5MzgsImV4cCI6MTY0MjQ4MzkzOCwiYXpwIjoibElQVU1YVjBhaHNGNWFRcmdZeGk2NThCZTNGbUZKZnAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.IcKYuat-G3L5K83IndHUKVuzlq_8R8ebjYOQr98MKE6LsKeqs-sOYcBPek9L9CNcqF5NTXyIYpjuzfNZhq-HBoCITNcomxFp1P2b769j1__2wi6hhiDWs21WHmgDt23hPOmp_AgtfaXazSjYOH91zwKv1GUYzTcTfkUjRAm3-C66rca-NuUuIXBeS95S3Cr8arrM6vYmw24fGZeLdKUEzklfhpogIY4qlzcq3E1Oukn_Lk07Pco1BvnEFrj5sEjOB-nZ8D-5sHnRg1ITFWEqKf_onuXFCLnZ1BdXvzZlkEDISokHyYFvbIB90J27mAS-ZyQq9vH8vqg9j9ZpjUrs-Q'
        #self.token_e = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVtd2J5S05DRklKMThIWXJZaDNyYSJ9.eyJpc3MiOiJodHRwczovL2Rldi11MWJ2YXp0OS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkZGE4ODNkMTg4ZDgwMDZlYTQ5YTg1IiwiYXVkIjoiY2Fwc3RvbmVfaW1hZ2UiLCJpYXQiOjE2NDI0MTE4NTUsImV4cCI6MTY0MjQ4Mzg1NSwiYXpwIjoibElQVU1YVjBhaHNGNWFRcmdZeGk2NThCZTNGbUZKZnAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.ihPN5tFcqLB7iX9ZkXjFDWsEHe1JacCw9cuCcfTURS28QKQ9tUBb5fz0MpHI3nnSKUTQ5lU22BadBkyc9CiPw7MR83Kp3SvKwfb_cs-t5tniRmzJEx2P1PQVwXVzfuJXPybw3t02vO_m8hJPLv6I435p-VJGnBMfuvf8bs8sWukxx96eTpyGd429pfi3pO5ck9NsLAXkRHpM4hSAVVnX90vbzMx_5TEIY8er9SFF4JFa1TJwiyBvErFqLqALYHvaNl6GjyoR_PZhaQ9J8_kBMRs-5a1NLJKltglicFuSVuhf-IZCNJaYDCW-rmYwKJy5rAhLq_zC_9ju5adXg6ji6A"
        
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

    # Get all available actors 
    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) # Check that status code is 200
        self.assertEqual(data['success'], True) # Check that the success of the body is true
        self.assertTrue(data['actors']) # Check that there are actors in the list

    # Get actor by id      


    # Delete actor with id 'actor_id'
    def test_delete_actor(self):
        res = self.client().delete('actors/9', headers={'Authorization': format(self.token_cd)}) # Delete actor with actor_id=8
        data = json.loads(res.data)

        actor = Actors.query.filter(Actors.id == 2).one_or_none() # Check that the question is no longer in the database
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success', True])
        self.assertTrue(data['deleted'])
        self.assertEqual(actor, None) # Check that actor no longer exists

    def test_404_actor_does_not_exist(self):

        res = self.client().delete('/actors/10000', headers={'Authorization': self.token_cd})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()