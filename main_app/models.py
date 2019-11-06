from django.db import models


class DataSet(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, primary_key=True)
    birthday = models.DateField()
