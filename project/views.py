from django.db.models import Q
# from drf_multiple_model.views import ObjectMultipleModelAPIView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
# from mypy.test import update
from django.urls import reverse

from project import models

# from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from django.db.models import CharField, Value
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Sum


# first page
@login_required
def index(request):
    if request.user.is_superuser:
        project = models.Project.objects.all()
        cost = 0
        for prj in project:
            if prj.money is not None:
                cost = cost + prj.money

        employee = models.Employee.objects.all()
        salary_sum = 0
        for emp in employee:
            if emp.salary is not None:
                salary_sum = salary_sum + emp.salary

        employee_user = get_object_or_404(models.Employee, user=request.user)

        tasks = models.Task.objects.all()

        salaries = models.MonthSalary.objects.all()
        salaries_sum = models.MonthSalary.objects.aggregate(Sum('money'))['money__sum']

        incomes = models.Income.objects.all()
        income_sum = incomes.filter(isOutcome=True).aggregate(Sum('money'))['money__sum']
        if income_sum is None:
            income_sum = 0
        outcome_sum = incomes.filter(isOutcome=False).aggregate(Sum('money'))['money__sum']
        if outcome_sum is None:
            outcome_sum = 0
        incomes_money = (income_sum) - (outcome_sum)

        debts = models.Debt.objects.all()
        debts_sum = models.Debt.objects.aggregate(Sum('price'))['price__sum']

        return render(request, 'project/index.html', {
            'project_count': project.count(),
            'project_total_money': cost,
            'employee_count': employee.count(),
            'employee_total_money': cost,
            'salary_sum': salary_sum,
            'task_count': tasks.count(),
            'salaries_count': salaries.count(),
            'salaries_sum': salaries_sum,
            'incomes_count': incomes.count(),
            'incomes_money': incomes_money,
            'income_sum': income_sum,
            'outcome_sum': outcome_sum,
            'debts_count': debts.count(),
            'debts_sum': debts_sum,
            'employee_user': employee_user,
        })
    else:
        employee = get_object_or_404(models.Employee, user=request.user)
        tasks = models.Task.objects.filter(employees=employee.id)
        workDays = models.WorkDay.objects.filter(employee=employee.id)
        salaries = models.MonthSalary.objects.filter(employee=employee.id)
        salaries_sum = salaries.aggregate(Sum('money'))['money__sum']
        debts = models.Debt.objects.filter(employee=employee.id)
        debt_sum = debts.filter(status__icontains='بدهی').aggregate(Sum('price'))['price__sum']
        if debt_sum is None:
            debt_sum = 0
        demand_sum = debts.filter(status__icontains='طلب').aggregate(Sum('price'))['price__sum']
        if demand_sum is None:
            demand_sum = 0
        debts_sum = demand_sum - debt_sum
        return render(request, 'project/employee_detail.html', {
            'employee': employee,
            'tasks': tasks,
            'workDays': workDays,
            'salaries': salaries,
            'salaries_sum': salaries_sum,
            'debts': debts,
            'debt_sum': debt_sum,
            'demand_sum': demand_sum,
            'debts_sum': debts_sum,
        })


#########################
#   project functions   #
#########################
class ProjectForm(ModelForm):
    class Meta:
        model = models.Project
        fields = ['title', 'projectOwner', 'pic', 'startDate', 'deadline', 'money']


# @login_required
@user_passes_test(lambda u: u.is_superuser)
def project_list(request):
    projects = models.Project.objects.all()
    data = {}
    return render(request, 'project/project_list.html', {'projects': projects})


# @login_required
@user_passes_test(lambda u: u.is_superuser)
def project_view(request, project_id):
    project = get_object_or_404(models.Project, pk=project_id)
    employees = models.Employee.objects.filter(task__project=project.id)
    tasks = models.Task.objects.filter(project=project.id)
    incomes = models.Income.objects.filter(project=project.id)
    incomes_sum = incomes.aggregate(Sum('money'))['money__sum']
    if incomes_sum is None:
        incomes_sum = 0
    if project.money is None:
        prj_mony = 0
    else:
        prj_mony = project.money
    money_res = prj_mony - incomes_sum
    return render(request, 'project/project_detail.html', {
        'project': project,
        'employees': employees,
        'tasks': tasks,
        'incomes': incomes,
        'incomes_sum': incomes_sum,
        'money_res': money_res,
    })


from django.utils.dateparse import parse_date


@user_passes_test(lambda u: u.is_superuser)
def project_create(request):
    # form = ProjectForm(request.POST or None)
    # if form.is_valid():
    #     form.save()
    #     return redirect('project:project-list')
    # return render(request, 'project/project_form.html', {'form': form})

    post_data = request.POST
    m_user = User.objects.get(id=post_data['user'])
    m_title = post_data['title']
    m_projectOwner = post_data['projectOwner']
    m_status = post_data['status']
    m_pic = None
    if post_data['isPicValid'] == 'true':
        m_pic = request.FILES['pic']
    try:
        m_startDate = (post_data['startDate'])
        m_deadline = (post_data['deadline'])
    except ValueError:
        m_startDate = str(timezone.now)
        m_deadline = str(timezone.now)

    m_money = int(post_data['money'])
    m_description = post_data['description']
    p = models.Project(user=m_user, title=m_title, projectOwner=m_projectOwner
                       , pic=m_pic, status=m_status
                       , startDate=m_startDate, deadline=m_deadline
                       , money=m_money, description=m_description)
    p.save()

    return redirect('project:project-list')


@user_passes_test(lambda u: u.is_superuser)
def project_update(request):
    post_data = request.POST
    m_user = User.objects.get(id=post_data['user'])
    m_title = post_data['title']
    m_projectOwner = post_data['projectOwner']
    m_startDate = timezone.now  # post_data['startDate']
    m_deadline = timezone.now  # post_data['deadline']
    m_status = post_data['status']
    m_money = int(post_data['money'])
    m_description = post_data['description']
    m_id = post_data['projectId']
    project = get_object_or_404(models.Project, pk=m_id)
    project.user = m_user
    project.title = m_title
    project.projectOwner = m_projectOwner
    if post_data['isPicValid'] == 'true':
        project.pic = request.FILES['pic']
    project.money = m_money
    project.description = m_description
    project.status = m_status
    project.save()

    return redirect('project:project-list')


@user_passes_test(lambda u: u.is_superuser)
def project_delete(request, project_id):
    project = get_object_or_404(models.Project, pk=project_id)
    project.delete()
    return redirect('project:project-list')


#########################
#   employee functions  #
#########################
# @login_required
# @user_passes_test(lambda u: u.is_superuser)
class EmployeeForm(ModelForm):
    class Meta:
        model = models.Employee
        fields = ['fullName', 'pic', 'startDate', 'salary', 'user']


# @login_required
@user_passes_test(lambda u: u.is_superuser)
def employee_list(request):
    employees = models.Employee.objects.all()
    return render(request, 'project/employee_list.html', {'employees': employees})


# @login_required
# @user_passes_test(lambda u: u.is_superuser)
@login_required
def employee_view(request, employee_id):
    if request.user.is_superuser:
        employee = get_object_or_404(models.Employee, pk=employee_id)
        tasks = models.Task.objects.filter(employees=employee.id)
        workDays = models.WorkDay.objects.filter(employee=employee.id)
        salaries = models.MonthSalary.objects.filter(employee=employee.id)
        salaries_sum = salaries.aggregate(Sum('money'))['money__sum']
        debts = models.Debt.objects.filter(employee=employee.id)
        debt_sum = debts.filter(status__icontains='بدهی').aggregate(Sum('price'))['price__sum']
        if debt_sum is None:
            debt_sum = 0
        demand_sum = debts.filter(status__icontains='طلب').aggregate(Sum('price'))['price__sum']
        if demand_sum is None:
            demand_sum = 0
        debts_sum = demand_sum - debt_sum
        return render(request, 'project/employee_detail.html', {
            'employee': employee,
            'tasks': tasks,
            'workDays': workDays,
            'salaries': salaries,
            'salaries_sum': salaries_sum,
            'debts': debts,
            'debt_sum': debt_sum,
            'demand_sum': demand_sum,
            'debts_sum': debts_sum,
        })
    else:

        employee = get_object_or_404(models.Employee, user=request.user)
        tasks = models.Task.objects.filter(employees=employee.id)
        workDays = models.WorkDay.objects.filter(employee=employee.id)
        salaries = models.MonthSalary.objects.filter(employee=employee.id)
        salaries_sum = salaries.aggregate(Sum('money'))['money__sum']
        debts = models.Debt.objects.filter(employee=employee.id)
        debt_sum = debts.filter(status__icontains='بدهی').aggregate(Sum('price'))['price__sum']
        if debt_sum is None:
            debt_sum = 0
        demand_sum = debts.filter(status__icontains='طلب').aggregate(Sum('price'))['price__sum']
        if demand_sum is None:
            demand_sum = 0
        debts_sum = demand_sum - debt_sum
        return render(request, 'project/employee_detail.html', {
            'employee': employee,
            'tasks': tasks,
            'workDays': workDays,
            'salaries': salaries,
            'salaries_sum': salaries_sum,
            'debts': debts,
            'debt_sum': debt_sum,
            'demand_sum': demand_sum,
            'debts_sum': debts_sum,
        })


@user_passes_test(lambda u: u.is_superuser)
def employee_create(request):
    form = EmployeeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('project:employee-list')
    return render(request, 'project/employee_form.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def employee_update(request, employee_id):
    employee = get_object_or_404(models.Employee, pk=employee_id)
    form = EmployeeForm(request.POST or None, instance=employee)
    if form.is_valid():
        form.save()
        return redirect('project:employee-list')
    return render(request, 'project/employee_form.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def employee_delete(request, employee_id):
    employee = get_object_or_404(models.Employee, pk=employee_id)
    employee.delete()
    return redirect('project:employee-list')


#########################
#   income functions  #
#########################
# @login_required
# @user_passes_test(lambda u: u.is_superuser)
class IncomeForm(ModelForm):
    class Meta:
        model = models.Income
        fields = ['project', 'pic', 'incomeDate', 'money', 'user']


import datetime
import dateutil.parser
from django.utils import timezone
import operator
import functools
from datetime import datetime


@login_required
# @user_passes_test(lambda u: u.is_superuser)
def income_list(request):
    if request.user.is_superuser or request.user.groups.filter(name='level1').exists():
        projects = models.Project.objects.all()
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page-size', 10)
        search = request.GET.get('search', '')

        start_date = request.GET.get('start_date', None)  # datetime.now().strftime('%Y-%m-%d')
        end_date = request.GET.get('end_date', None)
        is_income = request.GET.get('isIncome', None)
        is_outcome = request.GET.get('isOutcome', None)
        selected_projects = request.GET.get('selectedProjects', None)

        incomes = models.Income.objects.filter(Q(project__title__icontains=search)
                                               | Q(incomeDate__icontains=search)
                                               | Q(description__icontains=search)
                                               | Q(money__icontains=search)
                                               | Q(isOutcome__icontains=search)
                                               ).distinct()
        # filter data for level1 access (only access to outcome payment)
        if request.user.groups.filter(name='level1').exists():
            incomes = incomes.filter(isOutcome=True)

        # date range filter
        if start_date is not None and end_date is not None and start_date is not "" and end_date is not "":
            incomes = incomes.filter(incomeDate__range=[start_date, end_date]).distinct()

        # income/outcome filter
        if is_income is not None and is_outcome is not None and is_income is not "" and is_outcome is not "":
            if is_income == 'true' and is_outcome == 'true':
                pass
            elif is_income == 'true':
                incomes = incomes.filter(isOutcome=True).distinct()
            elif is_outcome == 'true':
                incomes = incomes.filter(isOutcome=False).distinct()

        # project filter
        projects_list = []
        if selected_projects is not None and selected_projects is not "":
            projects_list = selected_projects.split("_")
            incomes = incomes.filter(functools.reduce(operator.or_, (Q(project=x) for x in projects_list))).distinct()

        filter_param = {
            'start_date': start_date,
            'end_date': end_date,
            'is_income': is_income,
            'is_outcome': is_outcome,
            'projects_list': projects_list,
        }

        paginator = Paginator(incomes, page_size)
        try:
            incomes = paginator.page(page)
        except PageNotAnInteger:
            incomes = paginator.page(1)
        except EmptyPage:
            incomes = paginator.page(paginator.num_pages)

        return render(request, 'project/income/income_list.html', {'incomes': incomes,
                                                                   'projects': projects,
                                                                   'search': search,
                                                                   'page_size': page_size,
                                                                   'filter_param': filter_param,
                                                                   })
    else:
        return render(request, 'project/505.html')


# @login_required
@user_passes_test(lambda u: u.is_superuser)
def income_view(request, income_id):
    income = get_object_or_404(models.Income, pk=income_id)
    return render(request, 'project/income/income_detail.html', {'income': income})


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def income_create(request):
    if request.user.is_superuser or request.user.groups.filter(name='level1').exists():
        post_data = request.POST
        m_user = User.objects.get(id=post_data['user'])
        m_project = models.Project.objects.get(id=post_data['project'])
        m_pic = None
        if post_data['isIncomePicValid'] == 'true':
            m_pic = request.FILES['pic']
        try:
            m_incomeDate = (post_data['incomeDate'])
        except ValueError:
            m_incomeDate = str(timezone.now)

        m_money = int(post_data['money'])
        m_isOutcome = post_data['isOutcome']
        m_description = post_data['description']
        p = models.Income(user=m_user
                          , project=m_project
                          , pic=m_pic
                          , incomeDate=m_incomeDate
                          , money=m_money
                          , isOutcome=m_isOutcome
                          , description=m_description)
        p.save()

        return redirect('project:income-list')
    else:
        return render(request, 'project/505.html')


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def income_update(request):
    if request.user.is_superuser or request.user.groups.filter(name='level1').exists():
        post_data = request.POST
        m_user = User.objects.get(id=post_data['user'])
        m_project = models.Project.objects.get(id=post_data['project'])
        try:
            m_incomeDate = (post_data['incomeDate'])
        except ValueError:
            m_incomeDate = str(timezone.now)

        m_money = int(post_data['money'])
        if request.user.is_superuser:
            m_isOutcome = post_data['isOutcome']
        m_description = post_data['description']
        m_id = post_data['incomeId']

        income = get_object_or_404(models.Income, pk=m_id)
        income.user = m_user
        income.employee = m_project
        if post_data['isIncomePicValid'] == 'true':
            income.pic = request.FILES['pic']
        income.money = m_money
        if request.user.is_superuser:
            income.isOutcome = m_isOutcome
        income.incomeDate = m_incomeDate
        income.description = m_description
        income.save()

        return redirect('project:income-list')
    else:
        return render(request, 'project/505.html')


@user_passes_test(lambda u: u.is_superuser)
def income_delete(request, income_id):
    income = get_object_or_404(models.Income, pk=income_id)
    income.delete()
    return redirect('project:income-list')


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def task_list(request):
    if request.user.is_superuser:
        employees = models.Employee.objects.all()
        projects = models.Project.objects.all()
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page-size', 10)
        search = request.GET.get('search', '')

        start_date = request.GET.get('start_date', None)  # datetime.now().strftime('%Y-%m-%d')
        end_date = request.GET.get('end_date', None)
        is_income = request.GET.get('isIncome', None)
        is_outcome = request.GET.get('isOutcome', None)
        selected_projects = request.GET.get('selectedProjects', None)
        selected_employees = request.GET.get('selectedEmployees', None)
        selected_status = request.GET.get('selectedStatus', None)

        tasks = models.Task.objects.filter(Q(employees__fullName__icontains=search)
                                           | Q(project__title__icontains=search)
                                           | Q(taskDate__icontains=search)
                                           | Q(dueDate__icontains=search)
                                           | Q(description__icontains=search)
                                           | Q(title__icontains=search)
                                           | Q(status__icontains=search)
                                           )

        # date range filter
        if start_date is not None and end_date is not None and start_date is not "" and end_date is not "":
            tasks = tasks.filter(taskDate__range=[start_date, end_date]).distinct()

        # project filter
        projects_list = []
        if selected_projects is not None and selected_projects is not "":
            projects_list = selected_projects.split("_")
            tasks = tasks.filter(functools.reduce(operator.or_, (Q(project=x) for x in projects_list))).distinct()

        # employee filter
        employee_list = []
        if selected_employees is not None and selected_employees is not "":
            employee_list = selected_employees.split("_")
            tasks = tasks.filter(functools.reduce(operator.or_, (Q(employees=x) for x in employee_list))).distinct()

        # employee filter
        status_list = []
        if selected_status is not None and selected_status is not "":
            status_list = selected_status.split("_")
            tasks = tasks.filter(functools.reduce(operator.or_, (Q(status=x) for x in status_list))).distinct()

        filter_param = {
            'start_date': start_date,
            'end_date': end_date,
            'is_income': is_income,
            'is_outcome': is_outcome,
            'projects_list': projects_list,
            'employee_list': employee_list,
            'status_list': status_list,
        }

        paginator = Paginator(tasks, page_size)
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            tasks = paginator.page(1)
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)

        return render(request, 'project/task/task_list.html', {'tasks': tasks,
                                                               'employees': employees,
                                                               'projects': projects,
                                                               'search': search,
                                                               'filter_param': filter_param,
                                                               'page_size': page_size})
    else:
        employee = get_object_or_404(models.Employee, user=request.user)
        tasks = models.Task.objects.filter(employees=employee).distinct()
        projects = models.Project.objects.filter(task__in=tasks).distinct()
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page-size', 10)
        search = request.GET.get('search', '')

        start_date = request.GET.get('start_date', None)  # datetime.now().strftime('%Y-%m-%d')
        end_date = request.GET.get('end_date', None)
        selected_projects = request.GET.get('selectedProjects', None)
        selected_status = request.GET.get('selectedStatus', None)

        tasks = tasks.filter(Q(project__title__icontains=search)
                             | Q(taskDate__icontains=search)
                             | Q(dueDate__icontains=search)
                             | Q(description__icontains=search)
                             | Q(title__icontains=search)
                             | Q(status__icontains=search)
                             ).distinct()

        # date range filter
        if start_date is not None and end_date is not None and start_date is not "" and end_date is not "":
            tasks = tasks.filter(taskDate__range=[start_date, end_date]).distinct()

        # project filter
        projects_list = []
        if selected_projects is not None and selected_projects is not "":
            projects_list = selected_projects.split("_")
            tasks = tasks.filter(functools.reduce(operator.or_, (Q(project=x) for x in projects_list))).distinct()

        # status filter
        status_list = []
        if selected_status is not None and selected_status is not "":
            status_list = selected_status.split("_")
            tasks = tasks.filter(functools.reduce(operator.or_, (Q(status=x) for x in status_list))).distinct()

        filter_param = {
            'start_date': start_date,
            'end_date': end_date,
            'projects_list': projects_list,
            'status_list': status_list,
        }

        paginator = Paginator(tasks, page_size)
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            tasks = paginator.page(1)
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)

        return render(request, 'project/task/taskEmployee.html', {'tasks': tasks,
                                                                  'employee': employee,
                                                                  'projects': projects,
                                                                  'search': search,
                                                                  'filter_param': filter_param,
                                                                  'page_size': page_size})


@user_passes_test(lambda u: u.is_superuser)
def task_create(request):
    post_data = request.POST
    m_user = User.objects.get(id=post_data['user'])
    m_employee = models.Employee.objects.get(id=post_data['employee'])
    m_project = models.Project.objects.get(id=post_data['project'])
    m_pic = None
    if post_data['isTaskPicValid'] == 'true':
        m_pic = request.FILES['pic']
    try:
        m_taskDate = (post_data['taskDate'])
        m_dueDate = (post_data['dueDate'])
    except ValueError:
        m_taskDate = str(timezone.now)
        m_dueDate = str(timezone.now)

    m_title = post_data['title']
    m_status = post_data['status']
    m_description = post_data['description']
    p = models.Task(user=m_user
                    , employees=m_employee
                    , project=m_project
                    , pic=m_pic
                    , taskDate=m_taskDate
                    , dueDate=m_dueDate
                    , title=m_title
                    , status=m_status
                    , description=m_description)
    p.save()

    return redirect('project:task-list')


@user_passes_test(lambda u: u.is_superuser)
def task_update(request):
    post_data = request.POST
    m_user = User.objects.get(id=post_data['user'])
    m_employee = models.Employee.objects.get(id=post_data['employee'])
    m_project = models.Project.objects.get(id=post_data['project'])
    try:
        m_taskDate = (post_data['taskDate'])
        m_dueDate = (post_data['dueDate'])
    except ValueError:
        m_taskDate = str(timezone.now)
        m_dueDate = str(timezone.now)

    m_title = post_data['title']
    m_status = post_data['status']
    m_description = post_data['description']
    m_id = post_data['taskId']

    task = get_object_or_404(models.Task, pk=m_id)
    task.user = m_user
    task.employee = m_employee
    task.project = m_project
    if post_data['isTaskPicValid'] == 'true':
        task.pic = request.FILES['pic']
    task.taskDate = m_taskDate
    task.dueDate = m_dueDate
    task.description = m_description
    task.status = m_status
    task.title = m_title
    task.save()

    return redirect('project:task-list')


@user_passes_test(lambda u: u.is_superuser)
def task_delete(request, task_id):
    task = get_object_or_404(models.Task, pk=task_id)
    task.delete()
    return redirect('project:task-list')


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def salary_list(request):
    if request.user.is_superuser:
        employees = models.Employee.objects.all()
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page-size', 10)
        search = request.GET.get('search', '')

        salaries = models.MonthSalary.objects.filter(Q(employee__fullName__icontains=search)
                                                     | Q(money__icontains=search)
                                                     | Q(description__icontains=search)
                                                     | Q(workHour__icontains=search)
                                                     | Q(salaryDate__icontains=search)
                                                     )

        paginator = Paginator(salaries, page_size)
        try:
            salaries = paginator.page(page)
        except PageNotAnInteger:
            salaries = paginator.page(1)
        except EmptyPage:
            salaries = paginator.page(paginator.num_pages)

        return render(request, 'project/salary/salary_list.html', {'salaries': salaries,
                                                                   'employees': employees,
                                                                   'search': search,
                                                                   'page_size': page_size})
    else:
        employee = get_object_or_404(models.Employee, user=request.user)
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page-size', 10)
        search = request.GET.get('search', '')

        salaries = models.MonthSalary.objects.filter(Q(employee=employee)
                                                     & (Q(money__icontains=search)
                                                        | Q(description__icontains=search)
                                                        | Q(workHour__icontains=search)
                                                        | Q(salaryDate__icontains=search))
                                                     )

        paginator = Paginator(salaries, page_size)
        try:
            salaries = paginator.page(page)
        except PageNotAnInteger:
            salaries = paginator.page(1)
        except EmptyPage:
            salaries = paginator.page(paginator.num_pages)

        return render(request, 'project/salary/salaryEmployee.html', {'salaries': salaries,
                                                                      'employee': employee,
                                                                      'search': search,
                                                                      'page_size': page_size})


@user_passes_test(lambda u: u.is_superuser)
def salary_create(request):
    post_data = request.POST
    m_user = User.objects.get(id=post_data['user'])
    m_employee = models.Employee.objects.get(id=post_data['employee'])
    m_pic = None
    if post_data['isPicValid'] == 'true':
        m_pic = request.FILES['pic']
    try:
        m_salaryDate = (post_data['salaryDate'])
    except ValueError:
        m_salaryDate = str(timezone.now)

    m_money = int(post_data['money'])
    m_workHour = post_data['workHour']
    m_description = post_data['description']
    p = models.MonthSalary(user=m_user, employee=m_employee
                           , pic=m_pic
                           , salaryDate=m_salaryDate
                           , money=m_money, workHour=m_workHour, description=m_description)
    p.save()

    return redirect('project:salary-list')


@user_passes_test(lambda u: u.is_superuser)
def salary_delete(request, salary_id):
    salary = get_object_or_404(models.MonthSalary, pk=salary_id)
    salary.delete()
    return redirect('project:salary-list')


@user_passes_test(lambda u: u.is_superuser)
def salary_update(request):
    post_data = request.POST
    m_user = User.objects.get(id=post_data['user'])
    m_employee = models.Employee.objects.get(id=post_data['employee'])
    try:
        m_salaryDate = (post_data['salaryDate'])
    except ValueError:
        m_salaryDate = str(timezone.now)

    m_money = int(post_data['money'])
    m_workHour = post_data['workHour']
    m_description = post_data['description']
    m_id = post_data['salaryId']
    salary = get_object_or_404(models.MonthSalary, pk=m_id)
    salary.user = m_user
    salary.employee = m_employee
    salary.salaryDate = m_salaryDate
    if post_data['isPicValid'] == 'true':
        salary.pic = request.FILES['pic']
    salary.money = m_money
    salary.description = m_description
    salary.workHour = m_workHour
    salary.save()

    return redirect('project:salary-list')


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def debt_list(request):
    if request.user.is_superuser or request.user.groups.filter(name='level1').exists():
        employees = models.Employee.objects.all()
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page-size', 10)
        search = request.GET.get('search', '')

        debts = models.Debt.objects.filter(Q(employee__fullName__icontains=search)
                                           | Q(title__icontains=search)
                                           | Q(description__icontains=search)
                                           | Q(status__icontains=search)
                                           | Q(debtDate__icontains=search)
                                           | Q(paymentDebtDate__icontains=search)
                                           | Q(price__icontains=search)
                                           )

        paginator = Paginator(debts, page_size)
        try:
            debts = paginator.page(page)
        except PageNotAnInteger:
            debts = paginator.page(1)
        except EmptyPage:
            debts = paginator.page(paginator.num_pages)

        return render(request, 'project/debt/debt_list.html', {'debts': debts,
                                                               'employees': employees,
                                                               'search': search,
                                                               'page_size': page_size})
    else:
        employee = get_object_or_404(models.Employee, user=request.user)
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page-size', 10)
        search = request.GET.get('search', '')

        debts = models.Debt.objects.filter(Q(employee=employee)
                                           & (Q(title__icontains=search)
                                              | Q(description__icontains=search)
                                              | Q(status__icontains=search)
                                              | Q(debtDate__icontains=search)
                                              | Q(paymentDebtDate__icontains=search)
                                              | Q(price__icontains=search))
                                           )

        paginator = Paginator(debts, page_size)
        try:
            debts = paginator.page(page)
        except PageNotAnInteger:
            debts = paginator.page(1)
        except EmptyPage:
            debts = paginator.page(paginator.num_pages)

        return render(request, 'project/debt/debtEmployee.html', {'debts': debts,
                                                                  'employee': employee,
                                                                  'search': search,
                                                                  'page_size': page_size})


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def debt_create(request):
    if request.user.is_superuser or request.user.groups.filter(name='level1').exists():
        post_data = request.POST
        m_user = User.objects.get(id=post_data['user'])
        m_employee = models.Employee.objects.get(id=post_data['employee'])
        m_price = int(post_data['price'])
        m_title = post_data['title']
        m_status = post_data['status']
        m_description = post_data['description']

        try:
            m_debt_date = (post_data['debtDate'])
            m_payment_debt_date = (post_data['paymentDebtDate'])
        except ValueError:
            m_debt_date = str(timezone.now)
            m_payment_debt_date = str(timezone.now)

        p = models.Debt(user=m_user
                        , employee=m_employee
                        , title=m_title
                        , status=m_status
                        , price=m_price
                        , debtDate=m_debt_date
                        , paymentDebtDate=m_payment_debt_date
                        , description=m_description)
        p.save()

        return redirect('project:debt-list')
    else:
        return render(request, 'project/505.html')


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def debt_update(request):
    if request.user.is_superuser or request.user.groups.filter(name='level1').exists():
        post_data = request.POST
        m_user = User.objects.get(id=post_data['user'])
        m_employee = models.Employee.objects.get(id=post_data['employee'])
        try:
            m_debt_date = (post_data['debtDate'])
            m_payment_debt_date = (post_data['paymentDebtDate'])
        except ValueError:
            m_debt_date = str(timezone.now)
            m_payment_debt_date = str(timezone.now)

        m_price = int(post_data['price'])
        m_title = post_data['title']
        m_status = post_data['status']
        m_description = post_data['description']
        m_id = post_data['debtId']

        debt = get_object_or_404(models.Debt, pk=m_id)
        debt.user = m_user
        debt.employee = m_employee
        debt.debtDate = m_debt_date
        debt.paymentDebtDate = m_payment_debt_date
        debt.description = m_description
        debt.price = m_price
        debt.title = m_title
        debt.status = m_status
        debt.save()

        return redirect('project:debt-list')
    else:
        return render(request, 'project/505.html')


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def debt_delete(request, debt_id):
    if request.user.is_superuser or request.user.groups.filter(name='level1').exists():
        debt = get_object_or_404(models.Debt, pk=debt_id)
        debt.delete()
        return redirect('project:debt-list')
    else:
        return render(request, 'project/505.html')


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def company_equipment_list(request):
    if request.user.is_superuser or request.user.groups.filter(name='level1').exists():
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page-size', 10)
        search = request.GET.get('search', '')

        companyEquipments = models.CompanyEquipment.objects.filter(Q(title__icontains=search)
                                                                   | Q(description__icontains=search)
                                                                   | Q(buyDate__icontains=search)
                                                                   | Q(price__icontains=search)
                                                                   )

        paginator = Paginator(companyEquipments, page_size)
        try:
            companyEquipments = paginator.page(page)
        except PageNotAnInteger:
            companyEquipments = paginator.page(1)
        except EmptyPage:
            companyEquipments = paginator.page(paginator.num_pages)

        return render(request, 'project/companyEquipment_list.html', {'companyEquipments': companyEquipments,
                                                                      'search': search,
                                                                      'page_size': page_size})
    else:
        return render(request, 'project/505.html')


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def company_equipment_create(request):
    if request.user.is_superuser or request.user.groups.filter(name='level1').exists():
        post_data = request.POST
        m_user = User.objects.get(id=post_data['user'])
        m_title = post_data['title']
        m_price = int(post_data['price'])
        m_pic = None
        if post_data['isEqmPicValid'] == 'true':
            m_pic = request.FILES['pic']
        try:
            m_buyDate = (post_data['buyDate'])
        except ValueError:
            m_buyDate = str(timezone.now)

        m_description = post_data['description']
        p = models.CompanyEquipment(user=m_user
                                    , title=m_title
                                    , price=m_price
                                    , pic=m_pic
                                    , buyDate=m_buyDate
                                    , description=m_description)
        p.save()

        return redirect('project:companyEquipment-list')
    else:
        return render(request, 'project/505.html')


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def company_equipment_update(request):
    if request.user.is_superuser or request.user.groups.filter(name='level1').exists():
        post_data = request.POST
        m_user = User.objects.get(id=post_data['user'])
        try:
            m_buyDate = (post_data['buyDate'])
        except ValueError:
            m_buyDate = str(timezone.now)

        m_price = int(post_data['price'])
        m_title = post_data['title']
        m_description = post_data['description']
        m_id = post_data['eqmId']

        eqm = get_object_or_404(models.CompanyEquipment, pk=m_id)
        eqm.user = m_user
        eqm.buyDate = m_buyDate
        eqm.price = m_price
        eqm.title = m_title
        eqm.description = m_description
        if post_data['isEqmPicValid'] == 'true':
            eqm.pic = request.FILES['pic']
        eqm.save()

        return redirect('project:companyEquipment-list')
    else:
        return render(request, 'project/505.html')


@user_passes_test(lambda u: u.is_superuser)
def company_equipment_delete(request, companyEquipment_id):
    eqm = get_object_or_404(models.CompanyEquipment, pk=companyEquipment_id)
    eqm.delete()
    return redirect('project:companyEquipment-list')


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def workDay_list(request):
    if request.user.is_superuser or request.user.groups.filter(name='level1').exists():
        employees = models.Employee.objects.all()
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page-size', 10)
        search = request.GET.get('search', '')

        start_date = request.GET.get('start_date', None)  # datetime.now().strftime('%Y-%m-%d')
        end_date = request.GET.get('end_date', None)
        selected_employees = request.GET.get('selectedEmployees', None)

        workdays = models.WorkDay.objects.filter(Q(employee__fullName__icontains=search)
                                                 | Q(description__icontains=search)
                                                 | Q(workDate__icontains=search)
                                                 | Q(workHour__icontains=search)
                                                 )

        # date range filter
        if start_date is not None and end_date is not None and start_date is not "" and end_date is not "":
            workdays = workdays.filter(workDate__range=[start_date, end_date]).distinct()

        # employee filter
        employee_list = []
        if selected_employees is not None and selected_employees is not "":
            employee_list = selected_employees.split("_")
            workdays = workdays.filter(
                functools.reduce(operator.or_, (Q(employee=x) for x in employee_list))).distinct()

        filter_param = {
            'start_date': start_date,
            'end_date': end_date,
            'employee_list': employee_list,
        }

        paginator = Paginator(workdays, page_size)
        try:
            workdays = paginator.page(page)
        except PageNotAnInteger:
            workdays = paginator.page(1)
        except EmptyPage:
            workdays = paginator.page(paginator.num_pages)

        return render(request, 'project/workDay/workDay_list.html', {'workdays': workdays,
                                                                     'employees': employees,
                                                                     'search': search,
                                                                     'page_size': page_size,
                                                                     'filter_param': filter_param})
    else:
        employee = get_object_or_404(models.Employee, user=request.user)
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page-size', 10)
        search = request.GET.get('search', '')

        start_date = request.GET.get('start_date', None)  # datetime.now().strftime('%Y-%m-%d')
        end_date = request.GET.get('end_date', None)

        workdays = models.WorkDay.objects.filter((Q(description__icontains=search)
                                                  | Q(workDate__icontains=search)
                                                  | Q(workHour__icontains=search))
                                                 & Q(employee=employee)
                                                 )

        # date range filter
        if start_date is not None and end_date is not None and start_date is not "" and end_date is not "":
            workdays = workdays.filter(workDate__range=[start_date, end_date]).distinct()

        filter_param = {
            'start_date': start_date,
            'end_date': end_date,
        }

        paginator = Paginator(workdays, page_size)
        try:
            workdays = paginator.page(page)
        except PageNotAnInteger:
            workdays = paginator.page(1)
        except EmptyPage:
            workdays = paginator.page(paginator.num_pages)

        return render(request, 'project/workDay/workDayOfEmployee.html', {'workdays': workdays,
                                                                          'employee': employee,
                                                                          'search': search,
                                                                          'page_size': page_size,
                                                                          'filter_param': filter_param})


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def workDay_create(request):
    if request.user.is_superuser or request.user.groups.filter(name='level1').exists():
        post_data = request.POST
        m_user = User.objects.get(id=post_data['user'])
        m_employee = models.Employee.objects.get(id=post_data['employee'])
        m_description = post_data['description']
        m_work_hour = (post_data['workHour'])

        try:
            m_work_date = (post_data['workDate'])
        except ValueError:
            m_work_date = str(timezone.now)

        p = models.WorkDay(user=m_user
                           , employee=m_employee
                           , workDate=m_work_date
                           , workHour=m_work_hour
                           , description=m_description)
        p.save()

        return redirect('project:workDay-list')
    else:
        return render(request, 'project/505.html')


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def workDay_update(request):
    if request.user.is_superuser or request.user.groups.filter(name='level1').exists():
        post_data = request.POST
        m_user = User.objects.get(id=post_data['user'])
        m_employee = models.Employee.objects.get(id=post_data['employee'])
        m_work_hour = (post_data['workHour'])

        try:
            m_work_date = (post_data['workDate'])
        except ValueError:
            m_work_date = str(timezone.now)

        m_description = post_data['description']
        m_id = post_data['workDayId']

        workDay = get_object_or_404(models.WorkDay, pk=m_id)
        workDay.user = m_user
        workDay.employee = m_employee
        workDay.workDate = m_work_date
        workDay.workHour = m_work_hour
        workDay.description = m_description
        workDay.save()

        return redirect('project:workDay-list')
    else:
        return render(request, 'project/505.html')


# @user_passes_test(lambda u: u.is_superuser)
@login_required
def workDay_delete(request, workDay_id):
    if request.user.is_superuser or request.user.groups.filter(name='level1').exists():
        eqm = get_object_or_404(models.WorkDay, pk=workDay_id)
        eqm.delete()
        return redirect('project:workDay-list')
    else:
        return render(request, 'project/505.html')


@user_passes_test(lambda u: u.is_superuser)
def financial(request):
    projects = models.Project.objects.all()
    for prj in projects:
        prj.paied = models.Income.objects.filter(project=prj.id).aggregate(Sum('money'))['money__sum']
        if prj.paied is None:
            prj.paied = 0
        prj.remin = prj.money - prj.paied
        prj.save()
    income_total = models.Project.objects.aggregate(Sum('money'))['money__sum']
    paied_total = models.Income.objects.aggregate(Sum('money'))['money__sum']
    remin_total = income_total - paied_total

    employees = models.Employee.objects.all()
    for emp in employees:
        if emp.salary is None:
            emp.salary = 0
        if emp.phone is None:
            emp.phone = "-"
        emp.total_salary = models.MonthSalary.objects.filter(employee=emp.id).aggregate(Sum('money'))['money__sum']
        if emp.total_salary is None:
            emp.total_salary = 0
        emp.total_debt = \
            models.Debt.objects.filter(employee=emp.id).filter(status__icontains='بدهی').aggregate(Sum('price'))[
                'price__sum']
        if emp.total_debt is None:
            emp.total_debt = 0
        emp.total_demand = \
            models.Debt.objects.filter(employee=emp.id).filter(status__icontains='طلب').aggregate(Sum('price'))[
                'price__sum']
        if emp.total_demand is None:
            emp.total_demand = 0
        emp.save()

    salary_total = employees.aggregate(Sum('salary'))['salary__sum']
    month_salary_total = models.MonthSalary.objects.aggregate(Sum('money'))['money__sum']
    debt_total = models.Debt.objects.filter(status__icontains='بدهی').aggregate(Sum('price'))['price__sum']
    demand_total = models.Debt.objects.filter(status__icontains='طلب').aggregate(Sum('price'))['price__sum']
    return render(request, 'project/financial.html',
                  {
                      'projects': projects,
                      'income_total': income_total,
                      'paied_total': paied_total,
                      'remin_total': remin_total,
                      'employees': employees,
                      'salary_total': salary_total,
                      'month_salary_total': month_salary_total,
                      'debt_total': debt_total,
                      'demand_total': demand_total,
                  })


def pageNotExist(request):
    return render(request, 'project/505.html')


@login_required
def transaction_list(request):
    if request.user.is_superuser or request.user.groups.filter(name='level1').exists():
        projects = models.Project.objects.all()
        employees = models.Employee.objects.all()
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page-size', 10)
        search = request.GET.get('search', '')

        start_date = request.GET.get('start_date', None)  # datetime.now().strftime('%Y-%m-%d')
        end_date = request.GET.get('end_date', None)
        is_income = request.GET.get('isIncome', None)
        is_outcome = request.GET.get('isOutcome', None)
        selected_projects = request.GET.get('selectedProjects', None)
        selected_employees = request.GET.get('selectedEmployees', None)

        transaction = models.Transaction.objects.filter(Q(project__title__icontains=search)
                                                        | Q(employee__fullName__icontains=search)
                                                        | Q(createdAt__icontains=search)
                                                        | Q(description__icontains=search)
                                                        | Q(type__icontains=search)
                                                        | Q(money__icontains=search)
                                                        ).distinct()
        # filter data for level1 access (only access to outcome payment)
        if request.user.groups.filter(name='level1').exists():
            transaction = transaction.filter(type="پرداختی")

        # date range filter
        if start_date is not None and end_date is not None and start_date is not "" and end_date is not "":
            transaction = transaction.filter(createdAt__range=[start_date, end_date]).distinct()

        # income/outcome filter
        # if is_income is not None and is_outcome is not None and is_income is not "" and is_outcome is not "":
        #     if is_income == 'true' and is_outcome == 'true':
        #         pass
        #     elif is_income == 'true':
        #         incomes = incomes.filter(isOutcome=True).distinct()
        #     elif is_outcome == 'true':
        #         incomes = incomes.filter(isOutcome=False).distinct()

        # project filter
        projects_list = []
        if selected_projects is not None and selected_projects is not "":
            projects_list = selected_projects.split("_")
            transaction = transaction.filter(functools.reduce(operator.or_, (Q(project=x) for x in projects_list))).distinct()

        # employee filter
        employees_list = []
        if selected_employees is not None and selected_employees is not "":
            employees_list = selected_employees.split("_")
            transaction = transaction.filter(functools.reduce(operator.or_, (Q(employee=x) for x in employees_list))).distinct()

        filter_param = {
            'start_date': start_date,
            'end_date': end_date,
            # 'is_income': is_income,
            # 'is_outcome': is_outcome,
            'projects_list': projects_list,
            'employees_list': employees_list,
        }

        paginator = Paginator(transaction, page_size)
        try:
            transaction = paginator.page(page)
        except PageNotAnInteger:
            transaction = paginator.page(1)
        except EmptyPage:
            transaction = paginator.page(paginator.num_pages)

        accounts = models.Account.objects.all();
        sub_accounts = models.SubAccount.objects.all();

        return render(request, 'project/transaction_list.html', {'transactions': transaction,
                                                                   'projects': projects,
                                                                   'employees': employees,
                                                                   'search': search,
                                                                   'page_size': page_size,
                                                                   'filter_param': filter_param,
                                                                   'accounts': accounts,
                                                                   'sub_accounts': sub_accounts,
                                                                   })
    else:
        return render(request, 'project/505.html')


@login_required
def transaction_create(request):
    if request.user.is_superuser or request.user.groups.filter(name='level1').exists():
        post_data = request.POST
        m_user = User.objects.get(id=post_data['user'])
        m_sourceAccount = models.SubAccount.objects.get(id=post_data['sourceAccount'])
        m_destinationAccount = models.SubAccount.objects.get(id=post_data['destinationAccount'])
        if post_data['project'] != '-1':
            m_project = models.Project.objects.get(id=post_data['project'])
        else:
            m_project = None
        if post_data['employee'] != '-1':
            m_employee = models.Employee.objects.get(id=post_data['employee'])
        else:
            m_employee = None
        m_pic = None
        if post_data['isTransactionPicValid'] == 'true':
            m_pic = request.FILES['pic']
        try:
            m_createdAt = (post_data['createdAt'])
        except ValueError:
            m_createdAt = str(timezone.now)

        m_money = int(post_data['money'])
        m_type = post_data['type']
        m_description = post_data['description']

        p = models.Transaction(user=m_user
                               , project=m_project
                               , employee=m_employee
                               , pic=m_pic
                               , type=m_type
                               , money=m_money
                               , createdAt=m_createdAt
                               , source=m_sourceAccount
                               , destination=m_destinationAccount
                               , description=m_description)
        p.save()

        return redirect('project:transaction-list')
    else:
        return render(request, 'project/505.html')