from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import utils, auth_token_required

from database import db

from user_datastore import user_datastore

class LoginUser(Resource):
    def post(self):

        login_cred = request.get_json()

        if not login_cred or not login_cred.get('username') or not login_cred.get('password'):
            result = {
                'message': 'Username and password are required.'
            }

            return make_response(
                jsonify(result),
                400
            )
        
        username = login_cred['username']
        password = login_cred['password']

        # Data validation
        user = user_datastore.find_user(username=username)
        if not user:
            # return jsonify({'message': 'User not found.'}), 404
            return make_response(
                jsonify({'message': 'User not found.'}),
                404
            )
        
        if not utils.verify_password(password, user.password):
            # return jsonify({'message': 'Invalid password.'}), 401
            return make_response(
                jsonify({'message': 'Invalid password.'}),
                401
            )
        
        auth_token = user.get_auth_token()

        utils.login_user(user)

        result = {
            'message': 'Login successful.',
            'auth_token': auth_token,
            'user': {
                'username': user.username,
                'email': user.email,
                'roles': [role.name for role in user.roles]
            }
        }

        return make_response(
            jsonify(result),
            200
        )
    

class LogoutUser(Resource):
    @auth_token_required
    def post(self):
        utils.logout_user()
        result = {
            'message': 'Logout successful.'
        }

        return make_response(
            jsonify(result),
            200
        )

class RegisterUser(Resource):
    def post(self):
         
        user_cred = request.get_json()

        # Data validation
        if not user_cred or not user_cred.get('username') or not user_cred.get('email') or not user_cred.get('password'):
            result = {
                'message': 'Username, email, and password are required.'
            }

            return make_response(
                jsonify(result),
                400
            )
        
        user = user_datastore.find_user(username = user_cred['username'])
        if user:
            result = {
                'message': 'Username already exists.'
            }

            return make_response(
                jsonify(result),
                400
            )

        user = user_datastore.find_user(email = user_cred['email'])
        if user:
            result = {
                'message': 'Email already exists.'
            }

            return make_response(
                jsonify(result),
                400
            )
        
        username = user_cred['username']
        email = user_cred['email']
        password = user_cred['password']

        if len(password) < 6:
            result = {
                'message': 'Password must be at least 6 characters long.'
            }

            return make_response(
                jsonify(result),
                400
            )
        
        user_role = user_datastore.find_role('user')

        user_datastore.create_user(
            username=username,
            email=email,
            password=password,
            roles = [user_role]
        )

        db.session.commit()

        result = {
            'message': 'User registered successfully.',
            'user': {
                'username': username,
                'email': email
            }
        }
        return make_response(
            jsonify(result),
            201
        )


