# Create your views here.
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.views.generic import FormView
from django.contrib.auth import logout

from push.forms import SignupForm
from push.forms import RegIdSubmitForm
from push.forms import HomeForm

import sys

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

