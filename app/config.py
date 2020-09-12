import os
import configparser

basedir = os.path.abspath(os.path.dirname(__file__))
configfile = 'config.cfg'
config = configparser.ConfigParser()
config.read(configfile)


class Config(object):
    global config
    SECRET_KEY = config['server']['appkey']
    base = config['base']['file']
    open(config['base']['file'], 'w').write('rrrr')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, base)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FILEPATH = os.path.abspath(os.getcwd()+config['app']['filepath'])
