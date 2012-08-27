from django import forms
from django.contrib.auth.models import User
from push.models import GCM_RegId
from push.models import PhoneModelInfo
from django.db import IntegrityError
from django.contrib.auth import authenticate

import json
import urllib2

import sys


class SignupForm(forms.Form):
    login_id = forms.CharField(max_length=30)
    password = forms.CharField(max_length=100)
    email = forms.EmailField()

    def process(self):
        cd = self.cleaned_data
        User.objects.create_user(cd['login_id'], cd['email'], cd['password'])
        
    

class RegIdSubmitForm(forms.Form):
    login_id = forms.CharField(max_length=30)
    password = forms.CharField(max_length=100)
    gcm_regid = forms.CharField(max_length=100)
    phone_model = forms.CharField(max_length=30)
    phone_manufacturer = forms.CharField(max_length=30)
    

    def process(self, user):
        cd = self.cleaned_data
        user = authenticate(username=cd['login_id'], password=cd['password'])
        if user is not None and user.is_active:
            try:
                phone_model, created = PhoneModelInfo.objects.get_or_create(
                    model=cd['phone_model'],manufacturer=cd['phone_manufacturer'])
                
                phone_model.save()
            except IntegrityError:
                print 'could not save phone model - integrity error'
     
            gcm_regid = GCM_RegId()
            gcm_regid.user = user
            gcm_regid.phone_model = phone_model
            gcm_regid.gcm_regid = cd['gcm_regid']
            gcm_regid.save()
            
class HomeForm(forms.Form):
    phones= forms.ChoiceField(label='Select phone', choices = (), required=True)
    message = forms.CharField(widget=forms.Textarea(), max_length=1000, required=True)

    def __init__(self, user, *args, **kwargs):
        super(HomeForm, self).__init__(*args, **kwargs)
        print >> sys.stderr, 'form init'
        
        self.fields['phones'].choices = [(ids.id, ids.phone_model.short_name) for ids in GCM_RegId.objects.filter(user=user)]
        
    def process(self, user):
        GCM_URL = 'https://android.googleapis.com/gcm/send'
        GCM_API_KEY = 'AIzaSyDzNpkQcpzyrsDFNP7nNeaUeugonX0hK-g'
        
        print >> sys.stderr,  self.cleaned_data
        
        cd = self.cleaned_data
        regid_id = cd['phones']
        gcm_regid = GCM_RegId.objects.filter(id=regid_id).get(id=regid_id)
        print >> sys.stderr,  gcm_regid.gcm_regid
        print >> sys.stderr,  gcm_regid.phone_model.short_name

        headers = {}
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = "key=%s" % GCM_API_KEY
        
        
        data = {}
        data["registration_ids"] = [gcm_regid.gcm_regid]
        data["data"] = {"key1" : "%s" % cd["message"] }
        data["collapse_key"] = "common_message"  #mandatory since 'time_to_live' is used
        data["time_to_live"] = 600

        data = json.dumps(data)
        print >> sys.stderr, data
        req = urllib2.Request(GCM_URL, data, headers)

        response = urllib2.urlopen(req)
        the_page = response.read()

        print >> sys.stderr, 'RESPONSE OF GCM REQUEST: %s' % response
        print >> sys.stderr, the_page
        
        
