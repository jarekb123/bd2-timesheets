from my_app import ma
from database.models import Employee
from database import schemas

import simplejson
from marshmallow import fields

class SimpleEmployeeSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'job_position')


class EmployeeSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Employee


class EmployeeFreetimeSchema(schemas.EmployeeFreetimeSchema):
    freetime_type = fields.Nested(schemas.FreetimeTypeSchema)