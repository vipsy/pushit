from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    security_question = models.CharField(max_length=30)
    security_answer = models.CharField(max_length=30)

    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class PhoneModelInfo(models.Model):
    model = models.CharField(max_length=30)
    manufacturer = models.CharField(max_length=30)
    short_name = models.CharField(max_length=30)

    class Meta:
        unique_together = (('model', 'manufacturer'),)
    

class GCM_RegId(models.Model):
    gcm_regid = models.CharField(max_length=200, unique=True)
    
    phone_model = models.ForeignKey(PhoneModelInfo)
    user = models.ForeignKey(User)

    
