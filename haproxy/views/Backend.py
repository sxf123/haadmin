from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from haproxy.models import Backend
from django.views.generic import View
from haproxy.forms import OptionAddForm
from haproxy.models import Option
from haproxy.forms import BackendAddForm

@login_required
@require_http_methods(['GET'])
def backend_list(request):
    backend_list = Backend.objects.all()
    context = {'backend_list': backend_list}
    return render(request,'haproxy/backend_list.html',context)

class BackendAdd(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        backend_add_form = BackendAddForm()
        self.context = {'backend_add_form': backend_add_form}
        return render(request,'haproxy/backend_add.html',self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        backend_add_form = BackendAddForm(request.POST)
        if backend_add_form.is_valid():
            name = backend_add_form.cleaned_data.get('name')
            instance = request.POST.getlist('instance')
            backend = Backend(
                name = name
            )
            backend.save()
            for i in instance:
                backend.instance.add(i)
            return HttpResponseRedirect(reverse('backend_list'))
        else:
            self.context = {'backend_add_form': backend_add_form}
            return render(request,'haproxy/backend_add.html',self.context)

class BackendOptionAdd(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        backend = Backend.objects.get(pk=kwargs.get('pk')).name
        option_add_form = OptionAddForm(initial={'backend': backend})
        self.context = {'option_add_form': option_add_form}
        return render(request,'haproxy/option_add.html',self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        backend = Backend.objects.get(pk=kwargs.get('pk')).name
        option_add_form = OptionAddForm(request.POST,initial={'backend': backend})
        if option_add_form.is_valid():
            item = option_add_form.cleaned_data.get('item')
            param = option_add_form.cleaned_data.get('param',None)
            option = Option(
                item = item,
                param = param,
                backend = Backend.objects.get(pk=kwargs.get('pk'))
            )
            option.save()
            return HttpResponseRedirect(reverse('backend_list'))
        else:
            self.context = {'option_add_form': option_add_form,'errors': option_add_form.errors}
            return render(request,'haproxy/option_add.html',self.context)

