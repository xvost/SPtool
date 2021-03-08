import os
import configobj

basedir = os.path.abspath(os.path.dirname(__file__))
configfile = 'config.cfg'
config = configobj.ConfigObj(configfile)

class Config(object):
    global config
    CURENT_DIR = os.getcwd()
    SECRET_KEY = config['server']['appkey']
    BASE_FILE = config['base']['file']
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(CURENT_DIR, BASE_FILE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FILEPATH = os.path.abspath(CURENT_DIR+config['app']['filepath'])
    UPLOAD = os.path.abspath(CURENT_DIR+config['app']['upload'])
    voices = config['voices']