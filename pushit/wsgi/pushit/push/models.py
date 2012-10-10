from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Devices(models.Model):
    user = models.ForeignKey(User)
    
    android_id = models.CharField(max_length=64, unique=True)
    alias = models.CharField(max_length=30)
    gcm_regid = models.CharField(max_length=200)
    
    model = models.CharField(max_length=30)
    oem = models.CharField(max_length=30)
    
    
class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    security_question = models.CharField(max_length=30)
    security_answer = models.CharField(max_length=30)
    default_device = models.ForeignKey(Devices, null=True)

    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
    

    
