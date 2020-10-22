import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from sqlalchemy.exc import SQLAlchemyError
from datetime import *
from password_keeper.module import *

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.route('/')
    def hello():
        return jsonify({
            "status": 200,
            "message": "Hello World",
        })

    @app.route('/user', methods=['POST'])
    def add_user():
        body = request.get_json()

        if(body is None):
            abort(422)

        username = body.get('username', None)
        password = body.get('password', None)

        if(username is None or password is None):
            abort(422)

        print(username, password)

        try:
            newUser = User(username=username, password=password)
            User.insert(newUser)

            return jsonify({
                "status": "account created",
            })

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/app/user/auth', methods=['POST'])
    def auth_user():
        body = request.get_json()

        if(body is None):
            abort(422)

        username = body.get('username', None)
        password = body.get('password', None)

        if(username is None or password is None):
            abort(422)

        try:
            user_query = User.query.filter(User.username == username).filter(
                User.password == password).one_or_none()

            if(user_query is None):
                abort(404)

            user = User.get_user_id(user_query)
            return jsonify({
                "userId": user["userId"]
            })

        except Exception as e:
            print("Exception", e)
            abort(422)

    @app.route('/app/sites', methods=['POST'])
    def add_password():
        body = request.get_json()

        if(body is None):
            abort(422)

        userId = request.args.get('user')
        username=body.get('username',None)
        password = body.get('password', None)
        website = body.get('website',None)
        if(username is None or password is None or website is None):
            abort(422)

        try:
            newPassword = Password(user_id=userId,website=website,username=username,password=password)
            Password.insert(newPassword)

            return jsonify({
                "status": "success",
            })

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/app/sites/list', methods=['GET'])
    def get_passwords():

        userId = request.args.get('user')

        try:
            password_query = Password.query.filter(Password.user_id == userId).all()

            Passwords = list(map(Password.details, password_query))

            return jsonify({
                "passwords": Passwords
            })

        except Exception as e:
            print(e)
            abort(422)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    return app


if __name__ == '__main__':
    app.run()




