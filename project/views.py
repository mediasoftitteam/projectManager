
from django.db.models import Q
# from drf_multiple_model.views import ObjectMultipleModelAPIView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
# from mypy.test import update
from django.db.models import Q

from project import models

# from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from django.db.models import CharField, Value
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# first page
def index(request):
    return render(request, 'project/index.html')


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
    return render(request, 'project/project_detail.html', {'project': project})


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
    m_pic = None
    if post_data['isPicValid'] == 'true':
        m_pic = request.FILES['pic']
    try:
        m_startDate = (post_data['startDate'])
        m_deadline = (post_data['deadline'])
    except ValueError:
        m_startDate = str(timezone.now)
        m_deadline = str(timezone.now)


    print("-----------")
    print(m_startDate)
    print(m_deadline)
    m_money = int(post_data['money'])
    m_description = post_data['description']
    p = models.Project(user=m_user, title=m_title, projectOwner=m_projectOwner
                       , pic=m_pic
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
    m_startDate = timezone.now #post_data['startDate']
    m_deadline = timezone.now #post_data['deadline']
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
@user_passes_test(lambda u: u.is_superuser)
def employee_view(request, employee_id):
    employee = get_object_or_404(models.Employee, pk=employee_id)
    return render(request, 'project/employee_detail.html', {'employee': employee})


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


# @login_required
@user_passes_test(lambda u: u.is_superuser)
def income_list(request):
    incomes = models.Income.objects.all()
    data = {}
    return render(request, 'project/income_list.html', {'incomes': incomes})


# @login_required
@user_passes_test(lambda u: u.is_superuser)
def income_view(request, income_id):
    income = get_object_or_404(models.Income, pk=income_id)
    return render(request, 'project/income_detail.html', {'income': income})


@user_passes_test(lambda u: u.is_superuser)
def income_create(request):
    form = IncomeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('project:income-list')
    return render(request, 'project/income_form.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def income_update(request, income_id):
    income = get_object_or_404(models.Income, pk=income_id)
    form = IncomeForm(request.POST or None, instance=income)
    if form.is_valid():
        form.save()
        return redirect('project:income-list')
    return render(request, 'project/income_form.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def income_delete(request, income_id):
    income = get_object_or_404(models.Income, pk=income_id)
    income.delete()
    return redirect('project:income-list')


@user_passes_test(lambda u: u.is_superuser)
def task_list(request):
    employees = models.Employee.objects.all()
    projects = models.Project.objects.all()
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page-size', 10)
    search = request.GET.get('search', '')

    tasks = models.Task.objects.filter(Q(employees__fullName__icontains=search)
                                                 | Q(project__title__icontains=search)
                                                 | Q(taskDate__icontains=search)
                                                 | Q(dueDate__icontains=search)
                                                 | Q(description__icontains=search)
                                                 | Q(title__icontains=search)
                                                 | Q(status__icontains=search)
                                                 )

    paginator = Paginator(tasks, page_size)
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    return render(request, 'project/task_list.html', {'tasks': tasks,
                                                        'employees': employees,
                                                        'projects': projects,
                                                        'search': search,
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


@user_passes_test(lambda u: u.is_superuser)
def salary_list(request):
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

    return render(request, 'project/salary_list.html', {'salaries': salaries,
                                                        'employees': employees,
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


@user_passes_test(lambda u: u.is_superuser)
def debt_list(request):
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

    return render(request, 'project/debt_list.html', {'debts': debts,
                                                        'employees': employees,
                                                        'search': search,
                                                        'page_size': page_size})


@user_passes_test(lambda u: u.is_superuser)
def debt_create(request):
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


@user_passes_test(lambda u: u.is_superuser)
def debt_update(request):
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


@user_passes_test(lambda u: u.is_superuser)
def debt_delete(request, debt_id):
    debt = get_object_or_404(models.Debt, pk=debt_id)
    debt.delete()
    return redirect('project:debt-list')
