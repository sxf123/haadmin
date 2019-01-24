from django.shortcuts import render
from django.views.generic import View
from haproxy.models import Instance
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from haproxy.forms import InstanceAddForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms import model_to_dict
from django.http import JsonResponse
from haproxy.models import Option
from haproxy.models import Acl
from haproxy.generate import render_frontend,render_backend
from haproxy.models import Server

@login_required
@require_http_methods(['GET'])
def instance_list(request):
    instance_list = Instance.objects.all()
    instance_name = [instance.name for instance in instance_list]
    instance_ip = [instance.ip for instance in instance_list]
    instance_cluster = set([instance.cluster for instance in instance_list])
    context = {'instance_list': instance_list,'instance_name': instance_name,'instance_ip': instance_ip,'instance_cluster': instance_cluster}
    return render(request, 'haproxy/instance_list.html', context)

@login_required
@require_http_methods(['POST'])
def instance_search_by_cluster(request):
    cluster = request.POST.get('cluster')
    instance = Instance.objects.filter(cluster=cluster)
    instance_list = [model_to_dict(i) for i in instance]
    return JsonResponse({'instance_list': instance_list})

@login_required
@require_http_methods(['POST'])
def instance_search_by_name(request):
    name = request.POST.get('name')
    instance = Instance.objects.filter(name=name)
    instance_list = [model_to_dict(i) for i in instance]
    return JsonResponse({'instance_list': instance_list})

@login_required
@require_http_methods(['POST'])
def instance_search_by_cluster_and_name(request):
    name = request.POST.get('name')
    cluster = request.POST.get('cluster')
    instance = Instance.objects.filter(name=name).filter(cluster=cluster)
    instance_list = [model_to_dict(i) for i in instance]
    return JsonResponse({'instance_list': instance_list})

class InstanceAdd(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        instance_add_form = InstanceAddForm()
        self.context = {'instance_add_form': instance_add_form}
        return render(request,'haproxy/instance_add.html',self.context)
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self,request,*args,**kwargs):
        instance_add_form = InstanceAddForm(request.POST)
        if instance_add_form.is_valid():
            instance = Instance(
                name = instance_add_form.cleaned_data.get('name'),
                ip = instance_add_form.cleaned_data.get('ip'),
                ha_version = instance_add_form.cleaned_data.get('ha_version'),
                cluster = instance_add_form.cleaned_data.get('cluster')
            )
            instance.save()
            return HttpResponseRedirect(reverse('instance_list'))
        else:
            self.context = {'instance_add_form': instance_add_form,'errors': instance_add_form.errors}
            return render(request,'haproxy/instance_add.html',self.context)

class InstanceUpdate(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get('id')
        instance = Instance.objects.get(pk=id)
        instance_dict = model_to_dict(instance)
        instance_update_form = InstanceAddForm(instance_dict)
        self.context = {'instance_update_form': instance_update_form}
        return render(request, 'haproxy/instance_update.html', self.context)
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self,request,*args,**kwargs):
        id = kwargs.get('id')
        instance = Instance.objects.get(pk=id)
        instance_update_form = InstanceAddForm(request.POST)
        if instance_update_form.is_valid():
            name = instance_update_form.cleaned_data.get('name')
            ip = instance_update_form.cleaned_data.get('ip')
            ha_version = instance_update_form.cleaned_data.get('ha_version')
            cluster = instance_update_form.cleaned_data.get('cluster')
            instance.name = name
            instance.ip = ip
            instance.ha_version = ha_version
            instance.cluster = cluster
            instance.save()
            return HttpResponseRedirect(reverse('instance_list'))
        else:
            self.context = {'instance_update_form': instance_update_form,'errors': instance_update_form.errors}
            return render(request,'haproxy/instance_update.html',self.context)

@login_required
@require_http_methods(["GET"])
def generate_frontend(request,instance):
    instance = Instance.objects.get(name=instance)
    frontend_list = list(instance.frontend_set.all().values('name','ip','port','mode','monitor_uri'))
    for frontend in frontend_list:
        options = list(Option.objects.filter(frontend__name=frontend['name']).values('item','param'))
        acls = list(Acl.objects.filter(frontend__name=frontend['name']).values('name','criterion','criterion_args','flags','value'))
        frontend['options'] = options
        frontend['acls'] = acls
    render_frontend('frontend.cfg.html',frontend_list,'frontend_erp.cfg')
    return HttpResponseRedirect(reverse('instance_list'))

@login_required
@require_http_methods(['GET'])
def generate_backend(request,instance):
    instance = Instance.objects.get(name=instance)
    backend_list = list(instance.backend_set.all().values('name'))
    for backend in backend_list:
        options = list(Option.objects.filter(backend__name=backend['name']).values('item','param'))
        servers = list(Server.objects.filter(backend__name=backend['name']).values('name','ip','port','check_interval','rise','fall','cookie','weight'))
        backend['options'] = options
        backend['servers'] = servers
    render_backend('backend.cfg.html',backend_list,'backend_erp.cfg')
    return HttpResponseRedirect(reverse('instance_list'))

