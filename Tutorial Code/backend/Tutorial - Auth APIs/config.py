class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///example.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'secret_key_here'
    SECURITY_PASSWORD_SALT = 'password_salt_here'