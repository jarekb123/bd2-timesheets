from my_app import ma
from database import models


class StageSchema(ma.ModelSchema):
    class Meta:
        model = models.Stage
