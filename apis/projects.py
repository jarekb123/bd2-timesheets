from my_app import api, db
from flask_restplus import Resource, Namespace
from database.models import Project
from database.schemas import ProjectSchema

projects_api = Namespace('projects', description="Projects related operations")


@api.route('/projects')
class AllProjects(Resource):
    projects_schema = ProjectSchema(many=True)
    project_schema = ProjectSchema()

    def get(self):
        all_projects = Project.query.all()
        return self.projects_schema.jsonify(all_projects)

    def post(self):
        new_project = self.project_schema.load(api.payload)
        db.session.add(new_project.data)
        db.session.commit()
        return {'result': 'Project added'}, 201

