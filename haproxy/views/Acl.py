from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from haproxy.models import Acl
from haproxy.forms import AclAddForm
from django.views.generic import View
from haproxy.models import Frontend
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

@login_required
@require_http_methods(['GET'])
def acl_list(request,frontend):
    acl = Acl.objects.filter(frontend__name=frontend)
    context = {'acl_list': acl,'frontend': frontend}
    return render(request,'haproxy/acl_list.html',context)

class AclAdd(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        frontend = kwargs.get('frontend')
        acl_add_form = AclAddForm(initial={'frontend':frontend})
        self.context = {'acl_add_form': acl_add_form}
        return render(request,'haproxy/acl_add.html',self.context)
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self,request,*args,**kwargs):
        frontend = kwargs.get('frontend')
        acl_add_form = AclAddForm(request.POST,initial={'frontend': frontend})
        if acl_add_form.is_valid():
            name = acl_add_form.cleaned_data.get('name')
            criterion = acl_add_form.cleaned_data.get('criterion')
            criterion_args = acl_add_form.cleaned_data.get('criterion_args',Nonee)
            flags = acl_add_form.cleaned_data.get('flags',None)
            value = acl_add_form.cleaned_data.get('value')
            frontend = acl_add_form.cleaned_data.get('frontend')
            print(frontend)
            acl = Acl(
                name = name,
                criterion = criterion,
                criterion_args = criterion_args,
                flags = flags,
                value = value,
                frontend = Frontend.objects.get(name=frontend)
            )
            acl.save()
            return HttpResponseRedirect(reverse('acl_list',kwargs={'frontend': frontend}))
        else:
            self.context = {'acl_add_form': acl_add_form,'errors': acl_add_form.errors}
            print(acl_add_form.errors)
            return render(request,'haproxy/acl_add.html',self.context)