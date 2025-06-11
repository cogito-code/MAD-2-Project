from flask import Flask, request, jsonify
from flask_cors import CORS  # Use `pip install flask_cors` to install CORS. This allows cross-origin requests.
# We will see the use of CORS in later videos.
from flask_security import Security
from flask_restful import Api

# In this video, we will create Authentication and CRUD APIs using Flask RESTful and Flask-Security.
# We would implement authentication token mechanism using Flask-Security.

from config import Config
from database import db
from user_datastore import user_datastore

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Security(app, user_datastore)

    api = Api(app)
    return app, api

def init_db(app):
    with app.app_context():
        db.create_all()

        admin_role = user_datastore.find_or_create_role(name='admin', description='Administrator role')
        user_role = user_datastore.find_or_create_role(name='user', description='User role')

        admin_user = user_datastore.find_user(username='admin')
        if not admin_user:
            user_datastore.create_user(
                username='admin',
                email = 'admin@gmail.com',
                password = 'admin123',
                roles=[admin_role, user_role]
            )

        db.session.commit()


app, api = create_app()
CORS(app)  # Enable CORS for the app

from auth_apis import LoginUser, LogoutUser
api.add_resource(LoginUser, '/api/login')
api.add_resource(LogoutUser, '/api/logout')

if __name__ == '__main__':
    init_db(app) 
    app.run(debug = True)