# Create your views here.
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.views.generic import FormView
from django.views.generic import View
from django.contrib.auth import logout
from django.contrib.auth import authenticate


from django.http import HttpResponse, HttpResponseForbidden,HttpResponseNotFound,\
    HttpResponseBadRequest

from push.forms import SignupForm
from push.forms import HomeForm

import sys
from push.models import Devices


class HomeView(FormView):
    template_name = "home.html"
    form_class = HomeForm
    success_url = 'home'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        print >> sys.stderr, form.errors
        print >> sys.stderr, args
        print >> sys.stderr, kwargs
    

        if form.is_valid():
            print >> sys.stderr, "Form Valid"
            return self.form_valid(form)
        else:
            print >> sys.stderr, "Form NOT Valid"
            return self.form_invalid(form, **kwargs)       
        
    def get_form(self, form_class):
        form = HomeForm(self.request.user, data=self.request.POST)
        return form
    
    def form_valid(self, form):
        form.process(self.request.user)
        print >> sys.stderr, "RegIdSubmitView form_valid"
        return super(HomeView, self).form_valid(form)
        
    
class LogoutView(RedirectView):
    url = "home"

    def get_redirect_url(self):
        logout(self.request)
        return self.url

    
class SignupView(FormView):
    template_name = "signup.html"
    form_class = SignupForm
    success_url = 'home'
    
    def form_valid(self, form):
        form.process()
        return super(SignupView, self).form_valid(form) 
    

class PushITView(TemplateView):
    template_name = "home.html"
    
###########################################################################################
#######################################    API    #########################################
###########################################################################################
class APIRegisterId(View):
    
    def dispatch(self, *args, **kwargs):
        return super(APIRegisterId, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        try:
            username=request.POST['username']
            password=request.POST['password']
            model = request.POST['device_model']
            oem = request.POST['device_oem']
            android_id = request.POST['android_id']
            gcm_regid = request.POST['gcm_regid']
        except LookupError as err:
            print >> sys.stderr, 'post request with missing params\n  %s' % str(err)
            return HttpResponseBadRequest(content = str(err))
            
        
        
        print >> sys.stderr, 'username=%s, password=%s, model=%s, oem=%s, android_id=%s, gcm_regid=%s' \
            %(username, password, model, oem, android_id, gcm_regid);
 
        p_user = authenticate(username=username, password=password)

        if(p_user is not None):
            try:
                device = Devices.objects.get(user=p_user, android_id=android_id)
            except Devices.DoesNotExist:
                print >> sys.stderr, 'device does not exist'
                device = None
            
            if(device is None):
                device = Devices(user=p_user, android_id=android_id, model=model, 
                                 oem=oem, gcm_regid=gcm_regid, alias=model)
                device.save()
                print >> sys.stderr, 'new device created android_id=%s', device.android_id
            else:
                device.gcm_regid = gcm_regid
                print >> sys.stderr, 'device updated, android_id=%s, \ngcm_regid=%s',
                (device.android_id, device.gcm_regid)
                    
            return HttpResponse(content = "REGISTERED")
            
        else :
            return HttpResponse(content = "BAD_USER_ID_OR_PASSWORD")


    def get(self, request, *args, **kwargs):
        #print >> sys.stderr, self.request
        return HttpResponseForbidden()
        
class APILogin(View):
    
    def dispatch(self, *args, **kwargs):
        return super(APILogin, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        username=request.POST['username']
        password=request.POST['password']
 
        p_user = authenticate(username=username, password=password)

        if(p_user is not None):
            return HttpResponse(content = "REGISTERED")     
        else :
            return HttpResponseNotFound()

        
    def get(self, request, *args, **kwargs):
        #print >> sys.stderr, self.request
        return HttpResponseForbidden()    
