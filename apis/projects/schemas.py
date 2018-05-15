from my_app import ma
from database.models import Project
import simplejson


class ProjectSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Project