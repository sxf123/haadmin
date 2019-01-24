from django.shortcuts import render
from django.views.generic import View
from haproxy.forms import LoginForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse

@login_required
def index(request):
    return render(request,'common/index.html')

class LoginView(View):
    def __init__(self):
        self.context = {}
    def get(self,request,*args,**kwargs):
        login_form = LoginForm()
        self.context = {'login_form': login_form}
        return render(request,'common/login.html',self.context)
    def post(self,request,*args,**kwargs):
        url = request.GET.get('next')
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = auth.authenticate(username=username,password=password)
            if user is not None and user.is_active:
                auth.login(request,user)
                if url is not None:
                    return HttpResponsePermanentRedirect(url)
                else:
                    return HttpResponsePermanentRedirect(reverse('index'))
            else:
                self.context = {'login_form': login_form,'errors': login_form.errors}
                return render(request,'common/login.html',self.context)
        else:
            self.context = {'login_form': login_form,'errors': login_form.errors}
            return render(request,'common/login.html',self.context)

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponsePermanentRedirect(reverse('login'))