from my_app import api
from flask_restplus import Resource, Namespace
from database.models import Project
from database.schemas import ProjectSchema

projects_api = Namespace('projects', description="Projects related operations")


@api.route('/projects')
class AllProjects(Resource):
    projects_schema = ProjectSchema(many=True)

    def get(self):
        all_projects = Project.query.all()
        return self.projects_schema.jsonify(all_projects)
