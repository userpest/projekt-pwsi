from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Address(models.Model):
	owner = models.ForeignKey(User)
	lat = models.FloatField('Latitude', blank = True, null=True)
	lon = models.FloatField('Longitude', blank=True, null=True)
	name = models.CharField(max_length=200)
	comment = models.CharField(max_length=200)

class SharedInfo(models.Model):
	addr = models.ForeignKey(Address)
	shared_user = models.ForeignKey(User)
