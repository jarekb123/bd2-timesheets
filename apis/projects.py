from my_app import api, db
from flask_restplus import Resource, Namespace
from database.models import Project as ProjectModel
from database.schemas import ProjectSchema

from apis.decorators import handle_map_error

projects_api = Namespace('projects', description="Projects related operations")


@api.route('/projects/')
class AllProjects(Resource):
    projects_schema = ProjectSchema(many=True)
    project_schema = ProjectSchema()

    def get(self):
        all_projects = ProjectModel.query.all()
        return self.projects_schema.jsonify(all_projects)

    @handle_map_error("Bad JSON request")
    def post(self):
        new_project = self.project_schema.load(api.payload)
        db.session.add(new_project.data)
        db.session.commit()
        return {'result': 'Project added'}, 201


@api.route('/projects/<int:id>')
class Project(Resource):
    project_schema = ProjectSchema()

    def get(self, id):
        project = ProjectModel.query.get(id)
        if project is None:
            return {'error': 'No such project'}, 404
        else:
            return self.project_schema.jsonify(project)

    @handle_map_error("Bad JSON request")
    def put(self, id):
        project = ProjectModel.query.get(id)
        if project is None:
            return {'error': 'No such project'}, 404
        updated_project = self.project_schema.load(api.payload, instance=project).data
        db.session.add(updated_project)
        db.session.commit()
        return {'result': 'Project {} updated'.format(id)}

    def delete(self, id):
        ProjectModel.query.filter_by(id=id).delete()
        db.session.commit()
        return {'result': 'Project {} deleted'.format(id)}
