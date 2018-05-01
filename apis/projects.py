from my_app import api, db
from flask_restplus import Resource, Namespace
from database.models import Project as ProjectModel
from database.schemas import ProjectSchema

projects_api = Namespace('projects', description="Projects related operations")


@api.route('/projects')
class AllProjects(Resource):
    projects_schema = ProjectSchema(many=True)
    project_schema = ProjectSchema()

    def get(self):
        all_projects = ProjectModel.query.all()
        return self.projects_schema.jsonify(all_projects)

    def post(self):
        new_project = self.project_schema.load(api.payload)
        db.session.add(new_project.data)
        db.session.commit()
        return {'result': 'Project added'}, 201


@api.route('/projects/<int:id>')
class Project(Resource):
    project_schema = ProjectSchema()

    def get(self, id):
        project = ProjectModel.query.filter_by(id=id).first()
        if project:
            return self.project_schema.jsonify(project)
        else:
            return {'error': 'No such project'}, 404