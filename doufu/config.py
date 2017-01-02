import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'The Python Language 3.5'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'sqlite.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAX_CONTENT_LENGTH = 3*1024*1024  #upload文件限制3M
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 994
    MAIL_USER_TLS = True
    MAIL_USERNAME = 'sguzch'
    MAIL_PASSWORD = 'wywywywy2013'

    @staticmethod
    def init_app(app):
        pass




