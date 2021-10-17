from django.db import models
from authentication.models import User
from django.contrib.postgres.fields import CIEmailField, ArrayField, JSONField

from negantime.models import BaseModel

# Create your models here.


class Blog(BaseModel):
    title = models.CharField(default='', max_length=128)
    content = models.TextField(null=True, blank=True)
    images = ArrayField(models.CharField(
        max_length=2048), null=True, blank=True)
    author = models.ForeignKey(
        User,  on_delete=models.PROTECT)

    class Meta:
        db_table = 'blog'

    def __str__(self):
        return '%s, %s' % (self.title, self.author.id)
