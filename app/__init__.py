import os
from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

for dir in Config.UPLOAD, Config.FILEPATH:
    try:
        os.mkdir(dir)
    except:
        #ToDo add log
        pass
