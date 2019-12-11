
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

from django.db.models import Sum


# first page
def index(request):
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

    tasks = models.Task.objects.all()

    salaries = models.MonthSalary.objects.all()
    salaries_sum = models.MonthSalary.objects.aggregate(Sum('money'))['money__sum']

    incomes = models.Income.objects.all()
    income_sum = incomes.filter(isOutcome='هزینه').aggregate(Sum('money'))['money__sum']
    if income_sum is None:
        income_sum = 0
    outcome_sum = incomes.filter(isOutcome='درآمد').aggregate(Sum('money'))['money__sum']
    if outcome_sum is None:
        outcome_sum = 0
    incomes_money = (income_sum) - (outcome_sum)

    debts = models.Debt.objects.all()
    debts_sum = models.Debt.objects.aggregate(Sum('price'))['price__sum']

    return render(request, 'project/index.html',{
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
    projects = models.Project.objects.all()
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page-size', 10)
    search = request.GET.get('search', '')

    incomes = models.Income.objects.filter(Q(project__title__icontains=search)
                                                 | Q(incomeDate__icontains=search)
                                                 | Q(description__icontains=search)
                                                 | Q(money__icontains=search)
                                                 | Q(isOutcome__icontains=search)
                                                 )

    paginator = Paginator(incomes, page_size)
    try:
        incomes = paginator.page(page)
    except PageNotAnInteger:
        incomes = paginator.page(1)
    except EmptyPage:
        incomes = paginator.page(paginator.num_pages)

    return render(request, 'project/income_list.html', {'incomes': incomes,
                                                        'projects': projects,
                                                        'search': search,
                                                        'page_size': page_size})


# @login_required
@user_passes_test(lambda u: u.is_superuser)
def income_view(request, income_id):
    income = get_object_or_404(models.Income, pk=income_id)
    return render(request, 'project/income_detail.html', {'income': income})


@user_passes_test(lambda u: u.is_superuser)
def income_create(request):
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


@user_passes_test(lambda u: u.is_superuser)
def income_update(request):
    post_data = request.POST
    m_user = User.objects.get(id=post_data['user'])
    m_project = models.Project.objects.get(id=post_data['project'])
    try:
        m_incomeDate = (post_data['incomeDate'])
    except ValueError:
        m_incomeDate = str(timezone.now)

    m_money = int(post_data['money'])
    m_isOutcome = post_data['isOutcome']
    m_description = post_data['description']
    m_id = post_data['incomeId']

    income = get_object_or_404(models.Income, pk=m_id)
    income.user = m_user
    income.employee = m_project
    if post_data['isIncomePicValid'] == 'true':
        income.pic = request.FILES['pic']
    income.money = m_money
    income.isOutcome = m_isOutcome
    income.incomeDate = m_incomeDate
    income.description = m_description
    income.save()

    return redirect('project:income-list')


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


@user_passes_test(lambda u: u.is_superuser)
def company_equipment_list(request):
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


@user_passes_test(lambda u: u.is_superuser)
def company_equipment_create(request):
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


@user_passes_test(lambda u: u.is_superuser)
def company_equipment_update(request):
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
    print("-----")
    print(m_id)

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


@user_passes_test(lambda u: u.is_superuser)
def company_equipment_delete(request, companyEquipment_id):
    eqm = get_object_or_404(models.CompanyEquipment, pk=companyEquipment_id)
    eqm.delete()
    return redirect('project:companyEquipment-list')


@user_passes_test(lambda u: u.is_superuser)
def workDay_list(request):
    employees = models.Employee.objects.all()
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page-size', 10)
    search = request.GET.get('search', '')

    workdays = models.WorkDay.objects.filter(Q(employee__fullName__icontains=search)
                                       | Q(description__icontains=search)
                                       | Q(workDate__icontains=search)
                                       | Q(workHour__icontains=search)
                                       )

    paginator = Paginator(workdays, page_size)
    try:
        workdays = paginator.page(page)
    except PageNotAnInteger:
        workdays = paginator.page(1)
    except EmptyPage:
        workdays = paginator.page(paginator.num_pages)

    return render(request, 'project/workDay_list.html', {'workdays': workdays,
                                                      'employees': employees,
                                                      'search': search,
                                                      'page_size': page_size})


@user_passes_test(lambda u: u.is_superuser)
def workDay_create(request):
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


@user_passes_test(lambda u: u.is_superuser)
def workDay_update(request):
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


@user_passes_test(lambda u: u.is_superuser)
def workDay_delete(request, workDay_id):
    eqm = get_object_or_404(models.WorkDay, pk=workDay_id)
    eqm.delete()
    return redirect('project:workDay-list')
