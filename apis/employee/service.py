from apis.employee.schemas import Employee, EmployeeSchema, SimpleEmployeeSchema
from my_app import db


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
    new_employee = EmployeeSchema.load(employee_json).data
    db.session.add(new_employee)
    db.session.commit()
    return new_employee, 200


def get_employee(id):
    """
    Get an employee

    :param id: An ID of an employee
    :return: Serialized Employee
    """
    employee = Employee.query.get(id)
    if employee:
        return EmployeeSchema.jsonify(employee)
    else:
        return {'erorr': 'Employee does not exist'}