import os
from flask import Flask, request, jsonify, abort
from models import setup_db, Actor, Movie
from flask_cors import CORS
import json

from auth import AuthError, requires_auth


def create_app(test_config=None):
    '''
    The backbone of the API
    '''
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
    Actor APIs
    '''
    @app.route('/actors')
    @requires_auth(permission='get:actors')
    def get_actors():
        '''
        Public API available to any visitors of the website
        '''
        try:
            actors = Actor.query.order_by(Actor.id).all()

            if len(actors) == 0:
                abort(404)

            try:
                return_actors = [actor.format() for actor in actors]

                return jsonify({
                    'success': True,
                    'actors': return_actors
                }), 200

            except Exception as E:
                abort(422)

        except Exception as E:
            abort(400)

    @app.route('/actors', methods=['POST'])
    @requires_auth(permission='post:actors')
    def create_actor():
        '''
        REQUIRES Authorization to CREATE NEW ACTORS
        take Actor object and commit itself to the database
        '''
        body = request.json
        new_name = body['name']
        new_age = body['age']
        new_gender = body['gender']

        if new_name is None:
            abort(400)

        try:
            actor = Actor(name=new_name,
                          age=new_age,
                          gender=new_gender)
            actor.insert()
            # new_actor = actor.format()

            return jsonify({
                'success': True,
                'actor': new_name
            }), 200

            # return jsonify({
            #     'success': True,
            #     'actor': "Your Mom",
            #     'name': new_name,
            #     'age': new_age,
            #     'gender': new_gender
            # }), 200
        except Exception as E:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth(permission='patch:actors')
    def update_actor(self, actor_id):
        '''
        API make EDITS to an EXISTING actor object.
        Will take request object and push changes to the database
        '''
        actor = Actor.query.filter(Actor.id == actor_id).one_or_more()

        if actor is None:
            abort(404)
        body = request.json

        if body is None:
            abort(400)
        new_name = body['name']
        new_age = body['age']
        new_gender = body['gender']

        try:
            if new_name is not None:
                actor.name = new_name
            if new_gender is not None:
                actor.gender = new_gender
            if new_age is not None:
                actor.age = new_age

            actor.update()

            return jsonify({
                'success': True,
                'actor': new_name
            }), 200
        except Exception as E:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actor(actor_id):
        '''
        Ability to delete actors from database
        '''
        # actor = Actor.query.filter(Actor.id == actor_id).one_or_more()
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)
        actor.delete()

        return jsonify({
            'success': True,
            'delete': actor_id
        }), 200

    '''
    Movie object APIs
    '''
    @app.route('/movies')
    @requires_auth(permission='get:movies')
    def get_movies():
        '''
        Public API that is available to any visitor of the website
        '''
        try:
            movies = Movie.query.order_by(Movie.id).all()

            if len(movies) == 0:
                abort(404)

            try:
                return_movies = [movie.format() for movie in movies]

                return jsonify({
                    'success': True,
                    'movies': return_movies
                })

            except Exception as E:
                abort(422)

        except Exception as E:
            abort(400)

    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='post:movies')
    def create_movie():
        '''
        REQUIRES AUTH to CREATE NEW movie object.
        - post:movies
        '''
        body = request.json
        new_title = body['title']
        new_year = body['year']
        new_month = body['month']
        new_day = body['day']
        new_genre = body['genre']

        if new_title is None or new_genre is None:
            abort(400)

        try:
            movie = Movie(title=new_title,
                          year=new_year,
                          month=new_month,
                          day=new_day,
                          genre=new_genre)
            movie.insert()
            # new_movie = movie.format()

            return jsonify({
                'success': True,
                'movie': new_title
            }), 200
        except Exception as E:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth(permission='patch:movies')
    def update_movie(movie_id):
        '''
        Make UPDATES to an existing movie object in the database
        takes parameter movie_id and uses it to query database
        '''
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        body = request.json
        new_title = body['title']
        new_year = body['year']
        new_month = body['month']
        new_day = body['day']
        new_genre = body['genre']

        try:
            if new_title is not None:
                movie.title = new_title
            if new_year is not None:
                movie.year = new_year
            if new_month is not None:
                movie.month = new_month
            if new_day is not None:
                movie.day = new_day
            if new_genre is not None:
                movie.genre = new_genre

            movie.update()

            # new_movie = [movie.format()]

            return jsonify({
                'success': True,
                'movie': new_title
            }), 200
        except Exception as E:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_movie(movie_id):
        '''
        REQUIRES AUTH to delete movie/row from the database.
        Utilizes passed in movie_id to search for row and remove it from the db
        '''
        movie = Movie.query.filter(Movie.id == movie_id).one_or_more()

        if movie is None:
            abort(404)

        movie.delete()

        return jsonify({
            'success': True,
            'delete': movie_id
        }), 200

    @app.errorhandler(400)
    def bad_request(error):
        '''
        general bad request error
        '''
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad_request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        '''
        Query/Search result had no return values
        '''
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'not_found'
        })

    @app.errorhandler(422)
    def unprocessable(error):
        '''
        Action not able to be processed
        '''
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        })

    @app.errorhandler(500)
    def server_error(error):
        '''
        Internal Server Error. Error in models.py
        '''
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal_server_error'
        })

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
