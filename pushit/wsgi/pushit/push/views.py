# Create your views here.
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.views.generic import FormView
from django.views.generic import View
from django.contrib.auth import logout
from django.contrib.auth import authenticate


from django.http import HttpResponse, HttpResponseForbidden,\
    HttpResponseNotFound

from push.forms import SignupForm
from push.forms import RegIdSubmitForm
from push.forms import HomeForm

import sys
from push.models import GCM_RegId, PhoneModelInfo


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
        
        if(form.is_bound):
            print >> sys.stderr, "Form is Bound"
        else:
            print >> sys.stderr, "Form is NOT Bound"

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
    

class RegIdSubmitView(FormView):
    form_class = RegIdSubmitForm
    template_name = 'submitregid.html'
    success_url = 'home'
        
    def form_valid(self, form):
        form.process(self.request.user)
        return super(RegIdSubmitView, self).form_valid(form)


class PushITView(TemplateView):
    template_name = "home.html"
    
###########################################################################################
#######################################    API    #########################################
###########################################################################################
class APIRegisterId(View):
    
    def dispatch(self, *args, **kwargs):
        return super(APIRegisterId, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):

        username=request.POST['username']
        password=request.POST['password']
        model = request.POST['model']
        manufacturer = request.POST['manufacturer']
 
        p_user = authenticate(username=username, password=password)

        if(p_user is not None):
            try:
                p_phonemodel = PhoneModelInfo.objects.get(model=model, manufacturer=manufacturer)
            except PhoneModelInfo.DoesNotExist:
                p_phonemodel = None
            
            if(p_phonemodel is None):
                p_phonemodel = PhoneModelInfo(model=model, manufacturer=manufacturer, short_name=model)
                p_phonemodel.save()
                print >> sys.stderr, p_phonemodel.model
            else:
                print >> sys.stderr, p_phonemodel
                
            m_regId = GCM_RegId(user=p_user, gcm_regid=request.POST['regid'], phone_model = p_phonemodel)
            m_regId.save()
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
