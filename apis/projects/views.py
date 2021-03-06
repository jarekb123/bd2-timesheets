from my_app import api, db, ma
from flask_restplus import Resource, Namespace, Model, fields
from database.models import Project as ProjectModel, Employee, ProjectEmployeeRole
from marshmallow_sqlalchemy import field_for
from apis.projects.service import *
from apis.projects.schemas import ProjectSchema, ProjectEmployeeRoleSchema, SprintSchema

from apis.decorators import handle_map_error

projects_api = Namespace('Projects API', description="Projects related operations", path='/projects')
project_model = api.model('ProjectApi', {
    'name': fields.String(required=True),
    'description': fields.String(required=True),
    'budget': fields.Float(required=True),
    'start_time': fields.DateTime(required=True),
    'finish_time': fields.DateTime()
})


@projects_api.route('/')
class AllProjects(Resource):
    def get(self):
        """ Get all projects """
        all_projects = get_all_projects()
        return ProjectSchema(many=True).jsonify(all_projects)

    @api.expect(project_model, validate=True)
    def post(self):
        """ Post new project """
        print(api.payload)
        new_project = ProjectSchema().load(data=api.payload).data
        new_project = add_project(new_project)
        if new_project.id:
            return ProjectSchema().jsonify(new_project)
        else:
            return {'error': 'Project is not added'}, 503


@projects_api.route('/<int:project_id>')
class Project(Resource):
    project_schema = ProjectSchema()

    def get(self, project_id):
        """ 
        Returns a project 
        """
        project = ProjectModel.query.get(project_id)
        if project is None:
            return {'error': 'No such project'}, 404
        else:
            return self.project_schema.jsonify(project)

    @handle_map_error("Bad JSON request")
    def put(self, project_id):
        """ Updates a project """
        return update_project(api.payload, project_id)

    def delete(self, project_id):
        """ Deletes a project """
        return delete_project(id)


employee_project_relation_model = api.model('Project-Employee Relation', {
    'employee_id': fields.Integer(),
    'employee_role_id': fields.Integer(),
    'rate': fields.Float()

})


@projects_api.route('/<int:project_id>/employees')
class Employees(Resource):
    """ Employees related to particular project """

    def get(self, project_id):
        """ Returns employees related to project """
        employees = ProjectEmployeeRole.query.filter_by(project_id=project_id).all()
        return ProjectEmployeeRoleSchema(many=True).jsonify(employees)

    @api.expect(employee_project_relation_model)
    def post(self, project_id):
        """ Post new employee-project relation """
        result = add_employee_to_project(project_id, api.payload)
        if result:
            return ProjectEmployeeRoleSchema().jsonify(result)
        return {'error': 'Employee is not added to project'}, 503

    @api.expect(employee_project_relation_model)
    def put(self, project_id):
        """ Updates employee role in project """
        return add_employee_to_project(project_id, api.payload)


@projects_api.route('/<int:project_id>/employees/<int:employee_id>')
class Employees(Resource):
    """Employee deleting"""

    def delete(self, project_id, employee_id):
        """Deletes employee from project"""
        return delete_employee(project_id, employee_id)


sprint_model = api.model('SprintApi', {
    'start_time': fields.DateTime(required=True),
    'finish_time': fields.DateTime()
})


@projects_api.route('/<int:project_id>/sprints')
class SprintsRoute(Resource):
    """Operations related to project sprints"""

    def get(self, project_id):
        """Shows project sprints"""
        sprints = get_sprints(project_id)
        return sprints

    @api.expect(sprint_model, validate=True)
    def post(self, project_id):
        """Creates new sprint"""
        new_sprint = api.payload
        result = add_sprint(project_id, new_sprint)
        return result


@projects_api.route('/<int:project_id>/sprints/<int:sprint_id>')
class SprintsRoute(Resource):
    """Operations related to project sprints"""

    def get(self, project_id, sprint_id):
        """Shows project sprint"""
        sprint = get_sprint(project_id, sprint_id)
        return sprint


@projects_api.route('/<int:project_id>/sprints/<int:sprint_id>/report')
class SprintReport(Resource):
    """Operations related to report generation for sprint"""

    def get(self, project_id, sprint_id):
        """Shows sprint report"""
        result = get_sprint_report(project_id, sprint_id)
        return result


task_model = api.model('TaskApi', {
    'stage_id': fields.Integer,
    'description': fields.String
})


@projects_api.route('/<int:project_id>/sprints/<int:sprint_id>/task')
class SprintTask(Resource):

    @api.expect(task_model, validate=True)
    def post(self, sprint_id, project_id):
        new_task = api.payload
        result = create_task(sprint_id, new_task)
        return result

    def get(self, sprint_id, project_id):
        result = get_tasks(sprint_id)
        return result


add_employee_model = api.model('AddEmployeeAPI', {
    'employee_id': fields.Integer
})


@projects_api.route('/<int:project_id>/sprints/<int:sprint_id>/task/<int:task_id>/employees')
class SprintTaskEmployees(Resource):
    """Task employees"""

    def get(self, project_id, sprint_id, task_id):
        """Show task employees"""
        task_employees = get_task_employees(task_id)
        return task_employees

    @api.expect(add_employee_model, validate=True)
    def post(self, project_id, sprint_id, task_id):
        """Add employee to task"""
        status = add_employee_task(api.payload, task_id)
        if status is None:
            return 'Employee added', 200
        return status

    @api.expect(add_employee_model, validate=True)
    def delete(self, project_id, sprint_id, task_id):
        """Delete employee from task"""
        status = delete_employee_task(api.payload, task_id)
        if status is None:
            return 'Employee deleted', 200
        return status, 404


@projects_api.route('/<int:project_id>/sprints/<int:sprint_id>/task/<int:task_id>/worklog')
class SprintTaskWorklog(Resource):
    """Task worklog"""

    def get(self, project_id, sprint_id, task_id):
        """Show task worklog"""
        task_worklog = get_task_worklog(task_id)
        return task_worklog
