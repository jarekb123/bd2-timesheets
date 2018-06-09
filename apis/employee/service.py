from apis.employee.schemas import Employee, EmployeeSchema, SimpleEmployeeSchema, EmployeeFreetimeSchema
from database.models import EmployeeFreetime, Worklog, ProjectEmployeeRole, Summarize
from database.schemas import SummarizeSchema, WorklogSchema
from my_app import db

from sqlalchemy.exc import DatabaseError
from sqlalchemy import func
import decimal



def get_all_employees():
    """
    Get all employees

    :return: List of employees
    """
    employees = Employee.query.all()
    return SimpleEmployeeSchema(many=True).jsonify(employees)


def add_employee(employee_json):
    """
    Add new employee

    :param employee_json: Employee serialized as JSON
    :return: New employee with ID or an error, HTTP response code
    """
    new_employee = EmployeeSchema().load(employee_json).data
    db.session.add(new_employee)
    db.session.commit()
    return new_employee, 200


def get_employee(employee_id):
    """
    Get an employee

    :param employee_id: An ID of an employee
    :return: Serialized Employee
    """
    employee = Employee.query.get(employee_id)
    if employee:
        return EmployeeSchema().jsonify(employee)
    else:
        return {'error': 'Employee does not exist'}, 404


def get_employee_freetime(employee_id):
    employee_freetime = EmployeeFreetime.query.filter_by(employee_id=employee_id).all()
    if employee_freetime:
        return EmployeeFreetimeSchema(many=True).jsonify(employee_freetime)
    else:
        return {'error': 'Employee does not have free days'}, 404


def add_employee_freetime(employee_id, freetime_json):
    freetime = EmployeeFreetime(
        employee_id,
        freetime_json['free_hours_sum'],
        freetime_json['freetime_date'],
        freetime_json['freetime_type_id']
    )
    try:
        db.session.add(freetime)
        db.session.commit()
        return EmployeeFreetimeSchema().jsonify(freetime)
    except DatabaseError:
        return {'error': 'Freetime did not add correctly'}, 503


def generate_employee_summary(employee_id, year, month):
    worklogs = Worklog.query.filter(Worklog.employee_id == employee_id,
                                    func.month(Worklog.work_date) == month,
                                    func.year(Worklog.work_date) == year).all()

    salary = decimal.Decimal(0.0)
    for worklog in worklogs:
        project_id = worklog.task.sprint.project_id
        employee_role = ProjectEmployeeRole.query.filter(ProjectEmployeeRole.project_id == project_id,
                                                         ProjectEmployeeRole.employee_id == employee_id).first()
        if project_id and employee_role:
            salary = salary + employee_role.rate * worklog.logged_hours
    summary = Summarize(employee_id, month, year, float(salary))
    try:
        db.session.add(summary)
        db.session.flush()
        if summary in db.session:
            db.session.commit()
            return SummarizeSchema().jsonify(summary)
    except DatabaseError:
        return {'error': 'Summary did not generate properly'}, 501


def get_employee_worklog(employee_id):

    worklogs = Worklog.query.filter(Worklog.employee_id == employee_id).all()

    if worklogs:
        return WorklogSchema(many=True).jsonify(worklogs)
    else:
        return {'error': 'Employee didnt log any work'}, 404