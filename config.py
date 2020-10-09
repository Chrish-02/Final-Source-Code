import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_string"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    UPLOAD_FOLDER = '/path/to/the/uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    OAUTH_CREDENTIALS={
        'google': {
            'id':  '551543222360-b440lrckpei7ml10ffu2f0het2u45to5.apps.googleusercontent.com',
            'secret': 'Y6M-dLGUafpifGRkU2--wsTs'
        }
    }