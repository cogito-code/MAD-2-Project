from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import utils, auth_token_required

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