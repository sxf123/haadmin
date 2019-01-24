from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from haproxy.models import UseBackend,Backend
from haproxy.forms import UseBackendAddForm
from haproxy.models import Frontend
from django.core.urlresolvers import reverse

@login_required
@require_http_methods(["GET"])
def use_backend_list(request,frontend):
    use_backend_list = UseBackend.objects.filter(frontend__name=frontend)
    context = {'use_backend_list': use_backend_list,'frontend': frontend}
    return render(request,'haproxy/use_backend_list.html',context)

class UseBackendAdd(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        frontend = kwargs.get('frontend')
        use_backend_add_form = UseBackendAddForm(initial={'frontend': frontend},frontend=frontend)
        self.context = {'use_backend_add_form': use_backend_add_form,'frontend': frontend}
        return render(request,'haproxy/use_backend_add.html',self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        frontend = kwargs.get('frontend')
        use_backend_add_form = UseBackendAddForm(request.POST,initial={'frontend': frontend},frontend=frontend)
        if use_backend_add_form.is_valid():
            backend = use_backend_add_form.cleaned_data.get('backend')
            frontend = use_backend_add_form.cleaned_data.get('frontend')
            acl_true = request.POST.getlist('acl_true')
            relationship = use_backend_add_form.cleaned_data.get('relationship')
            acl = ""
            use_backend = UseBackend(
                backend = Backend.objects.get(name=backend),
                frontend = Frontend.objects.get(name=frontend),
                acl = acl
            )
            use_backend.save()
            return HttpResponseRedirect(reverse('use_backend_list',kwargs={'frontend':frontend}))
        else:
            self.context = {'use_backend_add_form': use_backend_add_form,'errors': use_backend_add_form.errors}
            return render(request,'haproxy/use_backend_add.html',self.context)