from my_app import ma
from database.models import Project, ProjectEmployeeRole, Sprint, Task, Worklog, Employee
from database.schemas import EmployeeSchema, EmployeeRoleSchema, TaskSchema, WorklogSchema, ReportSchema

from marshmallow import fields
import simplejson


class SprintSchema(ma.ModelSchema):
    class Meta:
        model = Sprint


class ProjectSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Project


class ProjectEmployeeRoleSchema(ma.ModelSchema):
    class Meta:
        model = ProjectEmployeeRole

    employee = fields.Nested(EmployeeSchema, only=('id', 'first_name', 'last_name'), dump_only=True)
    employee_role = fields.Nested(EmployeeRoleSchema, dump_only=True)


class WorklogSchemaSimple(ma.ModelSchema):
    class Meta:
        model = Worklog

    employee = fields.Nested(EmployeeSchema, only=('first_name', 'last_name'), dump_only=True)
