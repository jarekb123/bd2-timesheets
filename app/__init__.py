from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restplus import Api

app = Flask(__name__)
app.config.from_object('my_app.settings')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

api = Api(app)