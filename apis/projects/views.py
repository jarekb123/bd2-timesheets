from my_app import api, db, ma
from flask_restplus import Resource, Namespace, Model, fields
from database.models import Project as ProjectModel, Employee, ProjectEmployeeRole
from database.schemas import  ProjectEmployeeRoleSchema
from marshmallow_sqlalchemy import field_for
from apis.projects.service import *
from apis.projects.schemas import ProjectSchema

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
        new_project = ProjectSchema.load(api.payload).data
        new_project = add_project(new_project)
        if new_project.id:
            return ProjectSchema.jsonify(new_project)
        else:
            return {'error': 'Project is not added'}, 503


@projects_api.route('/<int:id>')
class Project(Resource):
    project_schema = ProjectSchema()

    def get(self, id):
        """ 
        Returns a project 
        """
        project = ProjectModel.query.get(id)
        if project is None:
            return {'error': 'No such project'}, 404
        else:
            return self.project_schema.jsonify(project)

    @handle_map_error("Bad JSON request")
    def put(self, id):
        """ Updates a project """
        return update_project(api.payload, id)

    def delete(self, id):
        """ Deletes a project """
        return delete_project(id)


employee_project_relation_model = api.model('Project-Employee Relation', {
    'employee_id': fields.Integer(),
    'role_id': fields.Integer(),
    'rate': fields.Float()

})


@projects_api.route('/<int:id>/employees')
class Employees(Resource):
    """ Employees related to particular project """

    def get(self, id):
        """ Returns employees related to project """
        employees = ProjectEmployeeRole.query.filter_by(project_id=id).all()
        return ProjectEmployeeRoleSchema(many=True).jsonify(employees)

    @api.expect(employee_project_relation_model)
    def post(self, id):
        """ Post new employee-project relation """
            