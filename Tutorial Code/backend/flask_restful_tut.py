from flask import Flask, make_response, jsonify, request

# Flask RESTful is an extension for Flask that adds support for quickly building REST APIs.
# It provides tools for creating resources, handling requests, and formatting responses.

from flask_restful import Api, Resource

user_details = []

app = Flask(__name__)

api = Api(app)

class HelloWorld(Resource):
    def get(self, username=None):
        # data = {
        #     'message': "Hello, World!"
        # }
        # return make_response(jsonify(data), 201)
        if username is None:
            if not user_details:
                return make_response(jsonify({'message': 'No users found'}), 404)
            return make_response(jsonify(user_details), 200)
        
        for user in user_details:
            if user['user_name'] == username:
                return make_response(jsonify(user), 200)
            
        return make_response(jsonify({'message': 'User not found'}), 404)


    def post(self):
        credentials = request.get_json()

        #data validation
        if 'user_name' not in credentials or 'address' not in credentials:
            return make_response(jsonify({'message': 'Invalid data'}), 400)
        
        user_details.append(credentials)
        result ={
            'message': 'User added successfully',
            'user':{
                'user_name': credentials['user_name'],
                'address': credentials['address']
            }
        }
        return make_response(jsonify(result), 201)


    def delete(self):
        pass


api.add_resource(HelloWorld, '/api', '/api/<string:username>')


if __name__ == '__main__':
    app.run(debug=True)