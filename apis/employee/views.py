from my_app import api
from flask_restplus import Namespace, Resource
from apis.employee.service import *
from flask_restplus import fields
from apis.employee.schemas import SimpleEmployeeSchema, EmployeeSchema

api_description = 'Employees related operations '
employee_api = Namespace('Employee API', api_description, path='/employees')


employee_model = api.model('Employee Model', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'job_position': fields.String(required=True),
    'contract_finish_date': fields.Date()
})


@employee_api.route('/')
class EmployeeApi(Resource):

    def get(self):
        """ Get all employees """
        return get_all_employees()

    @api.expect(employee_model, validate=True)
    def post(self):
        """ Add new employee """
        return add_employee(api.payload)


@employee_api.route('/<int:employee_id>')
@employee_api.doc(params={'id': 'An ID of an employee'})
class EmployeeDetailsApi(Resource):

    def get(self, employee_id):
        """ Get details of an employee """
        return get_employee(employee_id)


freetime_model = api.model('Freetime Model', {
    'freetime_date': fields.Date(required=True),
    'free_hours_sum': fields.Integer(required=True),
    'freetime_type_id': fields.Integer(required=True)
})


@employee_api.route('/<int:employee_id>/freetime')
class EmployeeFreeTimeApi(Resource):

    def get(self, employee_id):
        """ Get employee's freetime (days off) """
        return get_employee_freetime(employee_id)

    @api.expect(freetime_model, validate=True)
    def post(self, employee_id):
        """ Add new freetime days for employee """
        return add_employee_freetime(employee_id, api.payload)


@employee_api.route('/<int:employee_id>/gen_report/<int:year>/<int:month>')
class GenerateSummaryApi(Resource):

    def get(self, employee_id, year, month):
        """ Generates and returns monthly summary of the employee"""
        return generate_employee_summary(employee_id, year, month)


@employee_api.route('/<int:employee_id>/worklogs')
class EmployeeWorklogsApi(Resource):

    def get(self, employee_id):
        """ Get employee's worklogs """
        return get_employee_worklog(employee_id)