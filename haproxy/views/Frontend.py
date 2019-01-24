from django.shortcuts import render
from haproxy.models import Frontend
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from haproxy.forms import FrontendAddForm
from haproxy.models import Instance
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from haproxy.generate import render_frontend
from haproxy.models import Acl
from haproxy.forms import OptionAddForm
from haproxy.models import Option

@login_required
@require_http_methods(['GET'])
def frontend_list(request):
    frontend_list = Frontend.objects.all()
    context = {'frontend_list': frontend_list}
    return render(request,'haproxy/frontend_list.html',context)

class FrontendAdd(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        frontend_add_form = FrontendAddForm()
        self.context = {'frontend_add_form': frontend_add_form}
        return render(request,'haproxy/frontend_add.html',self.context)
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self,request,*args,**kwargs):
        frontend_add_form = FrontendAddForm(request.POST)
        if frontend_add_form.is_valid():
            name = frontend_add_form.cleaned_data.get('name')
            ip = frontend_add_form.cleaned_data.get('ip')
            port = frontend_add_form.cleaned_data.get('port')
            mode = frontend_add_form.cleaned_data.get('mode')
            monitor_uri = frontend_add_form.cleaned_data.get('monitor_uri')
            instance = request.POST.getlist('instance')
            frontend = Frontend(
                name = name,
                ip = ip,
                port = port,
                mode = mode,
                monitor_uri = monitor_uri
            )
            frontend.save()
            for i in instance:
                frontend.instance.add(i)
            return HttpResponseRedirect(reverse('frontend_list'))
        else:
            self.context = {'frontend_add_form': frontend_add_form,'errors': frontend_add_form.errors}
            return render(request,'haproxy/frontend_add.html',self.context)

class FrontendOptionAdd(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        frontend = Frontend.objects.get(pk=kwargs.get('pk')).name
        option_add_form = OptionAddForm(initial={'frontend': frontend})
        self.context = {'option_add_form': option_add_form}
        return render(request,'haproxy/option_add.html',self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        frontend = Frontend.objects.get(pk=kwargs.get('pk')).name
        option_add_form = OptionAddForm(request.POST,initial={'frontend': frontend})
        if option_add_form.is_valid():
            item = option_add_form.cleaned_data.get('item')
            param = option_add_form.cleaned_data.get('param',None)
            option = Option(
                item = item,
                param = param,
                frontend = Frontend.objects.get(pk=kwargs.get('pk'))
            )
            option.save()
            return HttpResponseRedirect(reverse('frontend_list'))
        else:
            self.context = {'option_add_form': option_add_form,'errors': option_add_form.errors}
            return render(request,'haproxy/option_add.html',self.context)