from django.db import models

# Create your models here.
from django.db import models


class Msg(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    message = models.CharField(max_length=1000, blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    star=models.IntegerField(default=0)
    emotion=models.IntegerField()
    photo=models.CharField(max_length=50,null=True)

    class Meta:
        db_table = 'msg'