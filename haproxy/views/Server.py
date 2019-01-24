from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from haproxy.models import Server
from haproxy.forms import ServerAddForm
from haproxy.models import Backend

@login_required
@require_http_methods(["GET"])
def server_list(request,backend):
    server_list = Server.objects.filter(backend__name=backend)
    context = {'server_list': server_list,'backend': backend}
    return render(request,'haproxy/server_list.html',context)

class ServerAdd(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        backend = kwargs.get('backend')
        server_add_form = ServerAddForm(initial={'backend': backend})
        self.context = {'server_add_form': server_add_form,'backend': backend}
        return render(request,'haproxy/server_add.html',self.context)
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self,request,*args,**kwargs):
        backend = kwargs.get('backend')
        server_add_form = ServerAddForm(request.POST,initial={'backend': backend})
        if server_add_form.is_valid():
            name = server_add_form.cleaned_data.get('name')
            ip = server_add_form.cleaned_data.get('ip')
            port = server_add_form.cleaned_data.get('port')
            check_interval = server_add_form.cleaned_data.get('check_interval')
            rise = server_add_form.cleaned_data.get('rise')
            fall = server_add_form.cleaned_data.get('fall')
            cookie = server_add_form.cleaned_data.get('cookie',None)
            weight = server_add_form.cleaned_data.get('weight')
            backend = server_add_form.cleaned_data.get('backend')
            server = Server(
                name = name,
                ip = ip,
                port = port,
                check_interval = check_interval,
                rise = rise,
                fall = fall,
                cookie = cookie,
                weight = weight,
                backend = Backend.objects.get(name=backend)
            )
            server.save()
            return HttpResponseRedirect(reverse('server_list',kwargs={'backend': backend}))
        else:
            self.context = {'server_add_form': server_add_form,'errors': server_add_form.errors}
            return render(request,'haproxy/server_add.html',self.context)
