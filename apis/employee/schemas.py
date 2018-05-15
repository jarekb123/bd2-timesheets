from my_app import ma
from database.models import Employee
import simplejson


class SimpleEmployeeSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Employee
        fields = ('id', 'first_name', 'last_name')


class EmployeeSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Employee