import os
import unittest
import json
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from app import app
from models import setup_db, Actor, Movie

# load_dotenv()

casting_assistant_jwt = os.environ.get('Casting_Assistant_JWT')
casting_director_jwt = os.environ.get('Casting_Director_JWT')
executive_producer_jwt = os.environ.get('Executive_Producer_JWT')


class TestCase(unittest.TestCase):
    def setup(self):
        self.app = app
        self.testing = True
        self.client = self.app.test_client
        self.Director = os.getenv('Director')
        self.Actor = os.getenv('Actor')
        self.new_actor = {
            'name': 'Keeanu Reeves',
            'age': 100,
            'gender': 'male'
        }
        self.movies = {
            'title': 'Immortal',
            'year': 2020,
            'month': 1,
            'day': 1,
            'genre': 'Keeanu Reeves'
        }
        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass

    def test_fetch_all_actors_asActor(self):
        res = self.client().get('/actors',
                                headers={'Authorization':
                                         f'Bearer {self.Actor}'},
                                json=new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not_found')

    def test_create_new_actor_asDirector(self):
        res = self.client().post('/actors',
                                 headers={'Authorization':
                                          f'Bearer {self.Director}'},
                                 json=new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'success')

    def test_create_new_movies_asActor(self):
        res = self.client().post('/movies',
                                 headers={'Authorization':
                                          f'Bearer {self.Actor}'},
                                 json=self.movies)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], {
                         'code': 'unauthorized', 'description':
                         'Permission not found.'})

    def test_create_new_movies_asDirector(self):
        res = self.client().post('/movies',
                                 headers={'Authorization':
                                          f'Bearer {self.Director}'},
                                 json=self.movies)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_new_movies_actor(self):
        res = self.client().post('/movies',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.Actor)
                                 }, json=self.movies)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], {
                         'code': 'unauthorized', 'description':
                         'Permission not found.'})

    def test_create_new_movies_director(self):
        res = self.client().post('/movies',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.Director)
                                 }, json=self.movies)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], {
                         'code': 'unauthorized', 'description':
                         'Permission not found.'})

        def test_fetch_all_moviess_casting_actor(self):
            res = self.client().get('/movies',
                                    headers={
                                        "Authorization": "Bearer {}".format(
                                            self.Actor)
                                    })
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], {
                'code': 'unauthorized', 'description':
                'Permission not found.'})

if __name__ == '__main__':
    unittest.main()