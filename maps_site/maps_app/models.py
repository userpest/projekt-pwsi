from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Address(models.Model):
	owner = models.ForeignKey(User)
	lat = models.FloatField()
	lng = models.FloatField()
	name = models.CharField(max_length=200,blank=True)
	comment = models.CharField(max_length=200,blank=True)

class SharedInfo(models.Model):
	addr = models.ForeignKey(Address)
	shared_user = models.ForeignKey(User)
