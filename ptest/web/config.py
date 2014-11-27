__author__ = 'Andrey'


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = b'secret key'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ADMIN_PASSWORD = 'Admin'
    TITLE = 'Untitled contest'


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True