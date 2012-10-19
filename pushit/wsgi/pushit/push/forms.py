from django import forms
from django.contrib.auth.models import User
from push.models import Devices
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import SiteProfileNotAvailable

import json
import urllib2
import sys
from django.core import exceptions

class SignupForm(forms.Form):
    login_id = forms.CharField(max_length=30)
    password = forms.CharField(max_length=100)
    email = forms.EmailField()

    def process(self):
        cd = self.cleaned_data
        User.objects.create_user(cd['login_id'], cd['email'], cd['password'])

            
class HomeForm(forms.Form):
    device= forms.ChoiceField(label='Select device',choices=(), initial="", required=True)
    data = forms.CharField(widget=forms.Textarea(), max_length=1000, required=True)
    

    def __init__(self, user, *args, **kwargs):
        super(HomeForm, self).__init__(*args, **kwargs)
        print >> sys.stderr, 'form init'
        
        choices = [(device.id, device.alias) for device in Devices.objects.filter(user=user)]
      
        #had to do this idiot thing as setting 'initial' in a form field did not work'
        try:
            profile = user.get_profile()
            default_device = profile.default_device
            if(default_device is not None):
                print >> sys.stderr, 'setting intial device value %s' %str(default_device.id)
                choices.remove( (default_device.id, default_device.alias) )
                choices.insert(0, (default_device.id, default_device.alias) )
                
        except (ObjectDoesNotExist, SiteProfileNotAvailable) as e :
            pass  
        
        self.fields['device'].choices = choices  
 
        
    def process(self, user):
        GCM_URL = 'https://android.googleapis.com/gcm/send'
        GCM_API_KEY = 'AIzaSyDzNpkQcpzyrsDFNP7nNeaUeugonX0hK-g'
        
        print >> sys.stderr,  'in HomeForm:process '
        
        cd = self.data
        try:
            device_id = cd['device']
            message = cd['data']
            action_id = cd['action_id']
            
        except LookupError as err:
            print >> sys.stderr, 'post request with missing params\n  %s' % str(err)
            return
        
        try:
            device = Devices.objects.get(id=device_id)
            try:
                profile = user.get_profile()
                profile.default_device = device
                profile.save()
            except (ObjectDoesNotExist, SiteProfileNotAvailable) as e :
                print >> sys.stderr, 'Error in user-profile' % str(e)
                pass
                    
            headers = {}
            headers["Content-Type"] = "application/json"
            headers["Authorization"] = "key=%s" % GCM_API_KEY
                    
            data = {}
            data["registration_ids"] = [device.gcm_regid]
            data["data"] = { 'action_id':action_id, 'data':"%s" % message }
            data["collapse_key"] = action_id  #mandatory since 'time_to_live' is used
            data["time_to_live"] = 10*60 #in seconds #x*60=x minutes  
    
            data = json.dumps(data)
            print >> sys.stderr, data
            req = urllib2.Request(GCM_URL, data, headers)
    
            response = urllib2.urlopen(req)
            the_page = response.read()
    
            print >> sys.stderr, 'RESPONSE OF GCM REQUEST: %s' % response
            print >> sys.stderr, the_page
        
        except Devices.DoesNotExist:
            print >> 'ERROR: Device with id=%s does not exist' % device_id
            pass

        
#            
#class HomeForm(forms.Form):
#    device= forms.ChoiceField(label='Select device',choices=(),initial=(), required=True)
#    message = forms.CharField(widget=forms.Textarea(), max_length=1000, required=True)
#
#    def __init__(self, user, *args, **kwargs):
#        super(HomeForm, self).__init__(*args, **kwargs)
#        print >> sys.stderr, 'form init'
#        
#        self.fields['device'].choices = \
#            [(device.id, device.alias) for device in Devices.objects.filter(user=user)]
#      
#        try:
#            profile = user.get_profile()
#            default_device = profile.default_device
#            if(default_device is not None):
#                self.fields['device'].initial=(default_device.id, default_device.alias)
#                
#        except (ObjectDoesNotExist, SiteProfileNotAvailable) as e :
#            pass    
# 
#        
#    def process(self, user):
#        GCM_URL = 'https://android.googleapis.com/gcm/send'
#        GCM_API_KEY = 'AIzaSyDzNpkQcpzyrsDFNP7nNeaUeugonX0hK-g'
#        
#        print >> sys.stderr,  self.cleaned_data
#        
#        cd = self.cleaned_data
#        device_id = cd['device']
#        try:
#            device = Devices.objects.get(id=device_id)
#            try:
#                profile = user.get_profile()
#                profile.default_device = device
#                profile.save()
#            except (ObjectDoesNotExist, SiteProfileNotAvailable) as e :
#                pass
#                    
#            headers = {}
#            headers["Content-Type"] = "application/json"
#            headers["Authorization"] = "key=%s" % GCM_API_KEY
#                    
#            data = {}
#            data["registration_ids"] = [device.gcm_regid]
#            data["data"] = {"key1" : "%s" % cd["message"] }
#            data["collapse_key"] = "common_message"  #mandatory since 'time_to_live' is used
#            data["time_to_live"] = 600
#    
#            data = json.dumps(data)
#            print >> sys.stderr, data
#            req = urllib2.Request(GCM_URL, data, headers)
#    
#            response = urllib2.urlopen(req)
#            the_page = response.read()
#    
#            print >> sys.stderr, 'RESPONSE OF GCM REQUEST: %s' % response
#            print >> sys.stderr, the_page
#        
#        except Devices.DoesNotExist:
#            print >> 'ERROR: Device with id=%s does not exist' % device_id
#            pass
