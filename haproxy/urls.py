from django.conf.urls import url
from haproxy.views.Login import index,logout
from haproxy.views.Instance import instance_list,InstanceAdd,InstanceUpdate,instance_search_by_cluster,instance_search_by_name,instance_search_by_cluster_and_name,generate_frontend,generate_backend
from haproxy.views.Frontend import frontend_list,FrontendAdd,FrontendOptionAdd
from haproxy.views.Backend import backend_list,BackendOptionAdd,BackendAdd
from haproxy.views.Server import server_list,ServerAdd
from haproxy.views.Acl import acl_list,AclAdd
from haproxy.views.UseBackend import use_backend_list,UseBackendAdd

urlpatterns = [
    url(r'^$',index,name='index'),
    url(r'^logout/$',logout,name='logout'),
    url(r'^instance/list/$',instance_list,name='instance_list'),
    url(r'^instance/add/$',InstanceAdd.as_view(),name='instance_add'),
    url(r'^instance/update/(?P<id>[0-9]+)/$',InstanceUpdate.as_view(),name='instance_update'),
    url(r'^instance/search/cluster/$',instance_search_by_cluster,name='instance_search_by_cluster'),
    url(r'^instance/search/name/$',instance_search_by_name,name='instance_search_by_name'),
    url(r'^instance/search/name/cluster/$',instance_search_by_cluster_and_name,name='instance_search_by_cluster_and_name'),
    url(r'^instance/frontend/generate/(?P<instance>(.*))/$',generate_frontend,name='generate_frontend'),
    url(r'^instance/backend/generate/(?P<instance>(.*))/$',generate_backend,name='generate_backend'),
    url(r'^frontend/list/$',frontend_list,name='frontend_list'),
    url(r'^frontend/add/$',FrontendAdd.as_view(),name='frontend_add'),
    url(r'^frontend/option/add/(?P<pk>[0-9]+)/$',FrontendOptionAdd.as_view(),name='frontend_option_add'),
    url(r'^backend/list/$',backend_list,name='backend_list'),
    url(r'^backend/add/$',BackendAdd.as_view(),name='backend_add'),
    url(r'^backend/option/add/(?P<pk>[0-9]+)/$',BackendOptionAdd.as_view(),name='backend_option_add'),
    url(r'^server/list/(?P<backend>(.*))/$',server_list,name='server_list'),
    url(r'^server/add/(?P<backend>(.*))/$',ServerAdd.as_view(),name='server_add'),
    url(r'^acl/list/(?P<frontend>(.*))/$',acl_list,name='acl_list'),
    url(r'^acl/add/(?P<frontend>(.*))/$',AclAdd.as_view(),name='acl_add'),
    url(r'^use_backend/list/(?P<frontend>(.*))/$',use_backend_list,name='use_backend_list'),
    url(r'^use_backend/add/(?P<frontend>(.*))/$',UseBackendAdd.as_view(),name="use_backend_add")
]