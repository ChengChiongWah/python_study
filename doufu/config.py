#!/usr/bin/env python3.5
# coding=utf-8
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'The Python Language 3.5'
    #    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'sqlite.db')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:dfdfdfdf2013@localhost/doufu'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # upload文件限制1M
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

    @staticmethod
    def init_app(app):
        pass
