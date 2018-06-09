from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restplus import Api
from flask_marshmallow import Marshmallow
import logging


app = Flask(__name__)
app.config.from_object('my_app.settings')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

api = Api(app)

ma = Marshmallow(app)

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

from apis import error_handlers


from apis.projects.views import projects_api
api.add_namespace(projects_api)

from apis.employee.views import employee_api
api.add_namespace(employee_api)

from apis.worklog.views import ns as worklog_api
api.add_namespace(worklog_api)