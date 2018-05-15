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
        add_employee(api.payload)


@employee_api.route('/<int:id>')
@employee_api.doc(params={'id': 'An ID of an employee'})
class EmployeeDetailsApi(Resource):

    def get(self, id):
        """ Get details of an employee """
        return get_employee(id)
