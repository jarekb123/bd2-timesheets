from my_app import ma
from database.models import Project, ProjectEmployeeRole
from database.schemas import EmployeeSchema, EmployeeRoleSchema

from marshmallow import fields
import simplejson


class ProjectSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Project


class ProjectEmployeeRoleSchema(ma.ModelSchema):
    class Meta:
        model = ProjectEmployeeRole
    employee = fields.Nested(EmployeeSchema, only=('id', 'first_name', 'last_name'))
    employee_role = fields.Nested(EmployeeRoleSchema, only=['name'])