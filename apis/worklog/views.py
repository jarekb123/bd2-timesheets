from apis.worklog.service import *
from my_app import api

from flask_restplus import Resource, Namespace, fields

ns = Namespace('Worklog API', description='Worklogs operations', path='/worklog')


worklog_model = ns.model('Worklog Model', {
    'employee_id': fields.Integer(required=True),
    'task_id': fields.Integer(required=True),
    'description': fields.String(required=True),
    'work_date': fields.Date(required=True),
    'logged_hours': fields.Integer(required=True)
})


@ns.route('/')
class Worklog(Resource):

    @ns.expect(worklog_model, validate=True)
    def post(self, ):
        return log_work(api.payload)

    def get(self, ):
        return get_worklogs()



