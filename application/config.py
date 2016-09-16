# configuration file with three config subclasses

# create config class with local environment variables
class Config(object):
    DATABASE = {
        'name': 'wifi_db',
        'host': 'localhost',
        'user': 'root',
        'password': 'summer'
    }
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'shhhh'


# create production subclass to toggle DEBUG off
class ProductionConfig(Config):
    DEBUG = False

# create development subclass
class DevelopmentConfig(Config):
    DEVELOPMENT = True

# create testing subclass to toggle TESTING on
class TestingConfig(Config):
    TESTING = True

