import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie

casting_assistant_jwt = os.environ.get('Casting_Assistant_JWT')
casting_director_jwt = os.environ.get('Casting_Director_JWT')
executive_producer_jwt = os.environ.get('Executive_Producer_JWT')
# database_path = os.environ.get('DATABASE_URL_local')

casting_assistant_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZ \
CI6IndNcl9NTXA3VXFWOW8xdDFjVUFTTCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtdH \
lsZXIudXMuYXV0aDAuY29tLyIsInN1YiI6ImhUSWhja1FUVFdJbThsWkRVcVYwOEt5 \
cWZsVTJGMmUzQGNsaWVudHMiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLC \
JpYXQiOjE2MDgzOTY4NjgsImV4cCI6MTYwODQ4MzI2OCwiYXpwIjoiaFRJaGNrUVRU \
V0ltOGxaRFVxVjA4S3lxZmxVMkYyZTMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbH \
MiLCJwZXJtaXNzaW9ucyI6W119.L1AyZ1MofME36P2MfNRb6SR0KaKEdTXJVYFqcS7 \
-TcuethML73EByZ_Cd6XrYYdz0oXuPPwWv7npbi7f0GAuOSzqZSJxpGeuKyL0J6vwV \
7x7hUhsp8QTOSdH3c6T0lrEvrKsivHkn57gPlu_gDGlka_VMS7NmODrJhZUc-NuOfC \
4ri9qJK3I-9J5I9P0Zz8-NpihtyqnGQ6Pkne_i0EwesV_HlvV4ArzdWo79kbGdSm0J \
BtPgVPbUNUuYTDtcU0_IC-g9WSqpzAtFtaM2zs1XrGFXGldH6TWrMFmicVAWJteRYV \
vybne2JbJ7Jzt9F9Crhk_mstc6_z9LqFCs1DGPw'

casting_director_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZC \
I6IndNcl9NTXA3VXFWOW8xdDFjVUFTTCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtdHl \
sZXIudXMuYXV0aDAuY29tLyIsInN1YiI6ImhUSWhja1FUVFdJbThsWkRVcVYwOEt5c \
WZsVTJGMmUzQGNsaWVudHMiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJ \
pYXQiOjE2MDgzOTY3ODksImV4cCI6MTYwODQ4MzE4OSwiYXpwIjoiaFRJaGNrUVRUV \
0ltOGxaRFVxVjA4S3lxZmxVMkYyZTMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHM \
iLCJwZXJtaXNzaW9ucyI6W119.O2QEn1X_BkMIXj7PX8-nNk4qJT1KlGxVVIMf4-YF \
3Sqf0hsTyGo4V2rP9XsbHQR18V2-SGDCcQlJVVJWmYkNhuNRXpooUKwu-SOVzUd9Cf \
G4r1iK3sUInYvyCSCAQPDg_oVlY9xy4-r1hYHO18NX8x_SGDE0G7PvqFx1-Jc1ztTH \
StFYwG-_c9yRaP4l62JZrMl7x-yPYh9m6ZtSDlrdTmn1a_bL1AogP4hLWZ8FCvsgiq \
xH9EXYCIPFBi6ZPzF81Wl-gAs2WamSnbqUVIR2EzwvBcIIyKslf_NaqdUJfUwx8fZ- \
KJ023bc4PLN71Y4FqTW3J0FLITTg8BDlQAiNqg'

executive_producer_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtp \
ZCI6IndNcl9NTXA3VXFWOW8xdDFjVUFTTCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtd \
HlsZXIudXMuYXV0aDAuY29tLyIsInN1YiI6ImhUSWhja1FUVFdJbThsWkRVcVYwOEt \
5cWZsVTJGMmUzQGNsaWVudHMiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiL \
CJpYXQiOjE2MDgzOTY5OTEsImV4cCI6MTYwODQ4MzM5MSwiYXpwIjoiaFRJaGNrUVR \
UV0ltOGxaRFVxVjA4S3lxZmxVMkYyZTMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhb \
HMiLCJwZXJtaXNzaW9ucyI6W119.Rf3KMIKZt__erkhK2nRIYYWPQNP_CMorK78ru- \
AHe00D15PbZc_1wcaghuEsz187Ua4IO51KsfSnotN_v09-4eBlXgfkBwBJR1MVhN0v \
2vUoBXBsXBwhjpGTARRj8jcHTl9-6VhXJ64YOISadFMtAg0bJCWVqwdwI1AVDGZGX2 \
Ep85f90ugrSKREMwJtJUA4a2civ0Cu5MERPv1QB73YnvohA5UkZmC55rUZU6iABcyr \
Eor_Qj3ojTNvZumZNI3iMADGeUkEQXF7kwfaP-vB7A7f7A5fGPmp6dW-pEnKKpSzSl \
wMkUpyT2zVBOyiN0maQVbcCm29CNd-FhOskxD9mg'


class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = \
            "postgresql://postgres:postgres@localhost:5432/postgres"
        self.Casting_Assistant = casting_assistant_jwt
        self.Casting_Director = casting_director_jwt
        self.Executive_Producer = executive_producer_jwt

        setup_db(self.app)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors_as_casting_assistant(self):

        response = self.client().get('/actors', headers={
            'Authorization': 'Bearer ' + self.Casting_Assistant})
        self.assertEqual(response.status_code, 200)

    def test_get_actors_as_casting_director(self):
        response = self.client().get('/actors', headers={
            'Authorization': 'Bearer ' + self.Casting_Director})
        self.assertEqual(response.status_code, 200)

    def test_post_actor_as_casting_director(self):
        response = self.client().post('/actors', headers={
            'Authorization': 'Bearer ' + self.Casting_Director},
            json={
                "name": "Jim Bob",
                "age": 100,
                "gender": "male"
                })

        self.assertEqual(response.status_code, 200)

    def test_delete_actor_as_casting_assistant(self):
        response = self.client().delete('/actors/1', headers={
            'Authorization': 'Bearer ' + self.Casting_Assistant})
        data = json.loads(response.data)
        self.assertEqual(data['success'], False)

    def test_post_movie_as_casting_director(self):
        response = self.client().post('/movies', headers={
            'Authorization': 'Bearer ' + self.Casting_Director},
            json={
                "title": "Dumb and Dumber",
                "year": 2000,
                "month": 5,
                "day": 12,
                "genre": "comedy"
                })

        data = json.loads(response.data)
        self.assertEqual(data['success'], False)

    def test_post_movie_as_executive_producer(self):
        response = self.client().post('/movies', headers={
            'Authorization': 'Bearer ' + self.Executive_Producer},
            json={
                "title": "March of the Penguins",
                "year": 2010,
                "month": 3,
                "day": 15,
                "genre": "documentary"
                })

        self.assertEqual(response.status_code, 200)

    def test_get_movies_as_casting_assistant(self):
        response = self.client().get('/movies', headers={
            'Authorization': 'Bearer ' + self.Casting_Assistant})
        self.assertEqual(response.status_code, 200)

    def test_get_movies_as_executive_producer(self):
        response = self.client().get('/movies', headers={
            'Authorization': 'Bearer ' + self.Executive_Producer})
        self.assertEqual(response.status_code, 200)

    def test_delete_movie_as_casting_assistant(self):
        response = self.client().delete('/movies/1', headers={
            'Authorization': 'Bearer ' + self.Casting_Assistant})
        data = json.loads(response.data)
        self.assertEqual(data['success'], False)

    def test_patch_actor_as_casting_director(self):
        response = self.client().patch('/actor/1', headers={
            'Authorization': 'Bearer ' + self.Casting_Director},
            json={
                "name": "Bubba Gump",
                "age": 10,
                "gender": "male"
                })

        self.assertEqual(response.status_code, 200)

    def test_patch_movie_as_casting_assistant(self):
        response = self.client().patch('/movie/1', headers={
            'Authorization': 'Bearer ' + self.Casting_Assistant},
            json={
                "title": "Impress Your Friends With a Well-Trained Human!",
                "year": 2120,
                "month": 12,
                "day": 30,
                "genre": "Best Practices in Dealing with Humans"
                })

        data = json.loads(response.data)
        self.assertEqual(data['success'], False)


if __name__ == '__main__':
    unittest.main()
