from my_app import ma
from database import models
import simplejson


class EmployeeSchema(ma.ModelSchema):
    class Meta:
        model = models.Employee


class EmployeeFreetimeSchema(ma.ModelSchema):
    class Meta:
        model = models.EmployeeFreetime


class EmployeeReportSchema(ma.ModelSchema):
    class Meta:
        model = models.EmployeeReport


class EmployeeRoleSchema(ma.ModelSchema):
    class Meta:
        model = models.EmployeeRole


class FreetimeTypeSchema(ma.ModelSchema):
    class Meta:
        model = models.FreetimeType


class ProjectSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = models.Project


class ProjectEmployeeRoleSchema(ma.ModelSchema):
    class Meta:
        model = models.ProjectEmployeeRole


class SprintSchema(ma.ModelSchema):
    class Meta:
        model = models.Sprint


class ReportSchema(ma.ModelSchema):
    class Meta:
        model = models.Report


class StageSchema(ma.ModelSchema):
    class Meta:
        model = models.Stage


class SummarizeSchema(ma.ModelSchema):
    class Meta:
        model = models.Summarize


class TaskSchema(ma.ModelSchema):
    class Meta:
        model = models.Task


class WorklogSchema(ma.ModelSchema):
    class Meta:
        model = models.Worklog
