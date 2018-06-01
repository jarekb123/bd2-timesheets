from my_app import ma
from database.models import Project, ProjectEmployeeRole
import simplejson


class ProjectSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Project


class ProjectEmployeeRoleSchema(ma.ModelSchema):
    class Meta:
        model = ProjectEmployeeRole
