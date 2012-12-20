from django.db import models
from django.contrib.auth.models import User
from annoying.fields import AutoOneToOneField

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

@receiver(post_save, sender = User)
def user_created_callback(sender,instance,**kwargs):

	try:
		UsersMarkerOptions.objects.get(user=instance)
	except UsersMarkerOptions.DoesNotExist:
		UsersMarkerOptions.objects.create(user=instance)

@receiver(pre_delete, sender = User)
def user_deleted_callback(sender, instance,**kwargs):
	try:
		UsersMarkerOptions.objects.get(user=instance).delete()
	except:
		pass

# Create your models here.
class Address(models.Model):
	owner = models.ForeignKey(User)
	lat = models.FloatField()
	lng = models.FloatField()
	addr = models.CharField(max_length=200)
	name = models.CharField(max_length=200,blank=True)
	comment = models.CharField(max_length=200,blank=True)

class SharedInfo(models.Model):
	addr = models.ForeignKey(Address)
	shared_user = models.ForeignKey(User)

class UsersMarkerOptions(models.Model):
	user = models.OneToOneField(User,primary_key=True)
	showShared = models.NullBooleanField( default = True )
	showSaved = models.NullBooleanField(  default  = True )
