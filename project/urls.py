from django.conf.urls import url
from . import views

app_name = 'project'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # project urls
    url(r'^project-list/$', views.project_list, name='project-list'),
    url(r'^(?P<project_id>[0-9]+)/project-detail/$', views.project_view, name='project-detail'),
    url(r'^project-new/', views.project_create, name='project-create'),
    url(r'^project-update/$', views.project_update, name='project-update'),
    url(r'^(?P<project_id>[0-9]+)/project-delete/$', views.project_delete, name='project-delete'),

    # employee urls
    url(r'^employee-list/$', views.employee_list, name='employee-list'),
    url(r'^(?P<employee_id>[0-9]+)/employee-detail/$', views.employee_view, name='employee-detail'),
    url(r'^employee-new/', views.employee_create, name='employee-create'),
    url(r'^(?P<employee_id>[0-9]+)/employee-update/$', views.employee_update, name='employee-update'),
    url(r'^(?P<employee_id>[0-9]+)/employee-delete/$', views.employee_delete, name='employee-delete'),

    # income urls
    url(r'^income-list/$', views.income_list, name='income-list'),
    url(r'^(?P<income_id>[0-9]+)/income-detail/$', views.income_view, name='income-detail'),
    url(r'^income-new/', views.income_create, name='income-create'),
    url(r'^(?P<income_id>[0-9]+)/employee-update/$', views.income_update, name='income-update'),
    url(r'^(?P<income_id>[0-9]+)/employee-delete/$', views.income_delete, name='income-delete'),

    # tasks urls
    url(r'^task-list/$', views.task_list, name='task-list'),

    # salary urls
    url(r'^salary-list/$', views.salary_list, name='salary-list'),
    url(r'^salary-new/$', views.salary_create, name='salary-create'),
    url(r'^salary-update/$', views.salary_update, name='salary-update'),
    url(r'^(?P<salary_id>[0-9]+)/salary-delete/$', views.salary_delete, name='salary-delete'),
]
