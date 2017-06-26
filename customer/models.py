import uuid
from django.contrib.postgres.fields import JSONField
from django.db import models


class CustomerSetUp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    data = JSONField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
