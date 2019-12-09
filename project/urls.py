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
    url(r'^task-new/$', views.task_create, name='task-create'),
    url(r'^task-update/$', views.task_update, name='task-update'),
    url(r'^(?P<task_id>[0-9]+)/task-delete/$', views.task_delete, name='task-delete'),

    # salary urls
    url(r'^salary-list/$', views.salary_list, name='salary-list'),
    url(r'^salary-new/$', views.salary_create, name='salary-create'),
    url(r'^salary-update/$', views.salary_update, name='salary-update'),
    url(r'^(?P<salary_id>[0-9]+)/salary-delete/$', views.salary_delete, name='salary-delete'),

    # debt urls
    url(r'^debt-list/$', views.debt_list, name='debt-list'),
    url(r'^debt-new/$', views.debt_create, name='debt-create'),
    url(r'^debt-update/$', views.debt_update, name='debt-update'),
    url(r'^(?P<debt_id>[0-9]+)/debt-delete/$', views.debt_delete, name='debt-delete'),

    # CompanyEquipment
    url(r'^companyEquipment-list/$', views.company_equipment_list, name='companyEquipment-list'),
    url(r'^companyEquipment-new/$', views.company_equipment_create, name='companyEquipment-create'),
    url(r'^companyEquipment-update/$', views.company_equipment_update, name='companyEquipment-update'),
    url(r'^(?P<companyEquipment_id>[0-9]+)/companyEquipment-delete/$', views.company_equipment_delete,
        name='companyEquipment-delete'),

    # employee work days urls
    url(r'^workDay-list/$', views.workDay_list, name='workDay-list'),
    url(r'^workDay-new/$', views.workDay_create, name='workDay-create'),
    url(r'^workDay-update/$', views.workDay_update, name='workDay-update'),
    url(r'^(?P<workDay_id>[0-9]+)/workDay-delete/$', views.workDay_delete, name='workDay-delete'),
]
