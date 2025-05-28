from flask import Flask, jsonify, request
from flask_sqlalchmey import SQLAlchemy

#pip install flask_security_too  - Command to install 
from flask_security import UserMixin,RoleMixin, Security, SQLAlchemyUserDatastore

# Tutorial on Flask Security
# Flask-Security is an extension that provides security features for Flask applications.
# It includes features like user authentication, role management, and password hashing.

db = SQLAlchemy()

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

    # Additional fields for Flask-Security
    fs_uniquifier = db.Column(db.String(255), unique = True, nullable=False)
    fs_token_uniquifier = db.Column(db.String(255), unique = True, nullable=True)

    roles = db.relationship('Role', secondary='user_role', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'<User {self.username}>'
    
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Role {self.name}>'
    
class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)

    def __repr__(self):
        return f'<UserRole user_id={self.user_id} role_id={self.role_id}>'


app = Flask(__name__)
db.init(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///security.db'
app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'
app.config['SECRET_KEY'] = 'my_precious'



user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)







if __name__ == '__main__':
    app.run(debug=True)