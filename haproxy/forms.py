from django.forms import TextInput,PasswordInput,Select,SelectMultiple
from django import forms
from haproxy.models import Instance,Frontend,Backend,Acl

class LoginForm(forms.Form):
    username = forms.CharField(
        widget = TextInput(attrs={"id":"user","placeholder":u"用户名称","class":"form-control","style":"border: 1px solid rgba(255, 255, 255, 0.1);background: rgba(0, 0, 0, 0.1);border-radius: 5px;color: #fff;height: 50px;"}),
        error_messages = {"required":"用户名不能为空"}
    )
    password = forms.CharField(
        widget = PasswordInput(attrs={"id": "pwd", "placeholder": u"密码","class":"form-control","style":"border: 1px solid rgba(255, 255, 255, 0.1);background: rgba(0, 0, 0, 0.1);border-radius: 5px;color: #fff;height: 50px;"}),
        error_messages={'required': u"密码不能为空"}
    )

class InstanceAddForm(forms.Form):
    name = forms.CharField(
        widget = TextInput(attrs={'id':'name','class':'form-control','placeholder':'请输入实例名称'})
    )
    ip = forms.CharField(
        widget = TextInput(attrs={'id':'ip','class':'form-control','placeholder':'请输入实例IP地址'})
    )
    ha_version = forms.CharField(
        widget = TextInput(attrs={'id':'ha_version','class':'form-control','placeholder':'请输入haproxy版本'})
    )
    cluster = forms.CharField(
        widget = Select(attrs={'id':'cluster','class':'form-control'},choices=(('','请选择集群'),('erp_haproxy','ERP Haproxy'),('im_haproxy','IM Haproxy')))
    )

class FrontendAddForm(forms.Form):
    name = forms.CharField(
        widget = TextInput(attrs={'id':'name','class':'form-control','placeholder':'请输入frontend名称'})
    )
    ip = forms.CharField(
        widget = TextInput(attrs={'id':'ip','class':'form-control','placeholder':'请输入监听ip'})
    )
    port = forms.CharField(
        widget = TextInput(attrs={'id':'port','class':'form-control','placeholder':'请输入监听端口'})
    )
    mode = forms.CharField(
        widget = Select(attrs={'id':'mode','class':'form-control'},choices=(('','请选择模式'),('http','http'),('tcp','tcp')))
    )
    monitor_uri = forms.CharField(
        widget = TextInput(attrs={'id':'monitor_uri','class':'form-control','placeholder':'请输入健康检测地址'})
    )
    instance = forms.MultipleChoiceField(
        widget = SelectMultiple(attrs={'id':'instance','class':'form-control select2'})
    )

    def __init__(self,*args,**kwargs):
        super(FrontendAddForm,self).__init__(*args,**kwargs)
        instance_choices = list(Instance.objects.all().values_list('id','name'))
        self.fields['instance'].choices = instance_choices

class BackendAddForm(forms.Form):
    name = forms.CharField(
        widget = TextInput(attrs={'id':'name','class':'form-control','placeholder':'请输入Backend名称'})
    )
    instance = forms.MultipleChoiceField(
        widget = SelectMultiple(attrs={'id':'instance','class':'form-control select2'})
    )

    def __init__(self,*args,**kwargs):
        super(BackendAddForm,self).__init__(*args,**kwargs)
        instance_choices = list(Instance.objects.all().values_list('id','name'))
        instance_choices.insert(0,('','请选择'))
        self.fields['instance'].choices = instance_choices

class AclAddForm(forms.Form):
    name = forms.CharField(
        widget = TextInput(attrs={'id':'name','class':'form-control','placeholder':'请输入Acl名称'})
    )
    criterion = forms.CharField(
        widget =Select(attrs={'id':'criterion','class':'form-control'},choices=(('','请选择Acl规则'),('hdr','hdr'),('hdr_dom','hdr_dom'),('src','src'),('path_beg','path_beg')))
    )
    criterion_args = forms.CharField(
        widget = TextInput(attrs={'id':'criterion_args','class':'form-control','placeholder':'请输入Acl参数'}),required=False
    )
    flags = forms.CharField(
        widget = Select(attrs={'id':'flags','class':'form-control'},choices=(('','请输入flags'),('-i','-i'),('-f','-f'))),required=False
    )
    value = forms.CharField(
        widget = TextInput(attrs={'id':'value','class':'form-control','placeholder':'请输入acl value'})
    )
    frontend = forms.CharField(
        widget = Select(attrs={'id':'frontend','class':'form-control'}),disabled=True
    )
    def __init__(self,*args,**kwargs):
        super(AclAddForm,self).__init__(*args,**kwargs)
        frontend_list = list(Frontend.objects.all().values_list('name','name'))
        frontend_list.insert(0,('','请选择Frontend'))
        self.fields['frontend'].widget.choices = frontend_list

class ServerAddForm(forms.Form):
    name = forms.CharField(
        widget = TextInput(attrs={'id':'server','class':'form-control','placeholder':'请输入server名称'})
    )
    ip = forms.CharField(
        widget = TextInput(attrs={'id':'ip','class':'form-control','placeholder':'请输入Server IP'})
    )
    port = forms.CharField(
        widget = TextInput(attrs={'id':'port','class':'form-control','placeholder':'请输入Server port'})
    )
    check_interval = forms.CharField(
        widget = TextInput(attrs={'id':'check_interval','class':'form-control','placeholder':'请输入check_interval'})
    )
    rise = forms.CharField(
        widget = TextInput(attrs={'id':'rise','class':'form-control','placeholder':'请输入rise'})
    )
    fall = forms.CharField(
        widget = TextInput(attrs={'id':'fall','class':'form-control','placeholder':'请输入fall'})
    )
    cookie = forms.CharField(
        widget = TextInput(attrs={'id':'cookie','class':'form-control','placeholder':'请输入cookie'}),required=False
    )
    weight = forms.CharField(
        widget = TextInput(attrs={'id':'weight','class':'form-control','placeholder':'请输入weight'})
    )
    backend = forms.CharField(
        widget = Select(attrs={'id':'backend','class':'form-control'}),disabled=True
    )

    def __init__(self,*args,**kwargs):
        super(ServerAddForm,self).__init__(*args,**kwargs)
        backend_list = list(Backend.objects.all().values_list('name','name'))
        backend_list.insert(0,('','请选择backend'))
        self.fields['backend'].widget.choices = backend_list

option_choices = (
    ('','请选择option规则'),
    ('httpchk','httpchk'),
    ('forwardfor','forwardfor')
)

class OptionAddForm(forms.Form):
    item = forms.CharField(
        widget = Select(attrs={'id':'item','class':'form-control'},choices=option_choices)
    )
    param = forms.CharField(
        widget = TextInput(attrs={'id':'param','class':'form-control','placeholder':'请输入参数'}),required=False
    )
    frontend = forms.CharField(
        widget = Select(attrs={'id':'frontend','class':'form-control'}),disabled=True,required=False
    )
    backend = forms.CharField(
        widget = Select(attrs={'id':'backend','class':'form-control'}),disabled=True,required=False
    )

    def __init__(self,*args,**kwargs):
        super(OptionAddForm,self).__init__(*args,**kwargs)
        frontend_choices = list(Frontend.objects.all().values_list('name','name'))
        backend_choices = list(Backend.objects.all().values_list('name','name'))
        frontend_choices.insert(0,('','请选择frontend'))
        backend_choices.insert(0,('','请选择backend'))
        self.fields['frontend'].widget.choices = frontend_choices
        self.fields['backend'].widget.choices = backend_choices

class UseBackendAddForm(forms.Form):
    backend = forms.CharField(
        widget = Select(attrs={'id':'backend','class':'form-control'})
    )
    frontend = forms.CharField(
        widget = Select(attrs={'id':'frontend','class':'form-control'}),disabled=True
    )
    acl = forms.MultipleChoiceField(
        widget = SelectMultiple(attrs={'id':'acl','class':'form-control select2'})
    )
    relationship = forms.CharField(
        widget = Select(attrs={'id':'relationship','class':'form-control'},choices=(('','请选择acl逻辑'),('||','或'),(' ','与')))
    )

    def __init__(self,*args,**kwargs):
        frontend = kwargs.pop('frontend')
        super(UseBackendAddForm,self).__init__(*args,**kwargs)
        backend_list = list(Backend.objects.all().values_list('name','name'))
        frontend_list = list(Frontend.objects.all().values_list('name','name'))
        acl_list = list(Acl.objects.filter(frontend__name=frontend).values_list('name','name'))
        backend_list.insert(0,('','请选择backend'))
        frontend_list.insert(0,('','请选择frontend'))
        self.fields['backend'].widget.choices = backend_list
        self.fields['frontend'].widget.choices = frontend_list
        self.fields['acl'].choices = acl_list
