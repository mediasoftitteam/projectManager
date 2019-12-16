from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
import uuid


def scramble_uploaded_filename(instance, filename):
    extention = filename.split(".")[-1]
    return "{}.{}".format(uuid.uuid4(), extention)


class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, help_text='کاربر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان پروژه')
    projectOwner = models.CharField(max_length=120, null=True, blank=True, help_text='کارفرما')
    pic = models.ImageField('uploaded image', null=True, blank=True, upload_to=scramble_uploaded_filename, help_text='تصویر')
    startDate = models.DateField(default=timezone.now, help_text='شروع پروژه')
    deadline = models.DateField(default=timezone.now, help_text='تاریخ اتمام پروژه')
    money = models.BigIntegerField(null=True, blank=True, help_text='هزینه پروژه')
    description = models.CharField(max_length=120, null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["startDate"]

    def __str__(self):
        return  self.title

    @property
    def owner(self):
        return self.user


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    fullName = models.CharField(max_length=120, null=True, blank=True)
    pic = models.ImageField('uploaded image', null=True, blank=True, upload_to=scramble_uploaded_filename)
    startDate = models.DateField(default=timezone.now)
    salary = models.BigIntegerField(null=True, blank=True)
    position = models.CharField(max_length=120, null=True, blank=True, help_text='تخصص')
    education = models.CharField(max_length=120, null=True, blank=True, help_text='تحصیلات')
    activation = models.BooleanField(null=True, blank=True, help_text='وضعیت فعالیت')
    paymentType = models.CharField(max_length=120, null=True, blank=True, help_text='نوع پرداخت')
    phone = models.CharField(max_length=120, null=True, blank=True)
    address = models.CharField(max_length=120, null=True, blank=True)
    email = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        ordering = ["startDate"]

    def __str__(self):
        return str(self.user.username) + " - " + self.fullName

    @property
    def owner(self):
        return self.user


class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    pic = models.ImageField('uploaded image', null=True, blank=True, upload_to=scramble_uploaded_filename)
    incomeDate = models.DateField(default=timezone.now)
    money = models.BigIntegerField(null=True, blank=True)
    description = models.CharField(max_length=120, null=True, blank=True, help_text='توضیحات')
    isOutcome = models.CharField(max_length=50, null=True, blank=True, help_text='هزینه-درآمد')

    class Meta:
        ordering = ["incomeDate"]

    def __str__(self):
        return str(self.user.username) + " - " + self.project.title

    @property
    def owner(self):
        return self.user


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # employees = models.ManyToManyField(Employee)
    employees = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    taskDate = models.DateField(default=timezone.now)
    dueDate = models.DateField(default=timezone.now)
    description = models.CharField(max_length=120, null=True, blank=True, help_text='توضیحات')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    status = models.CharField(max_length=50, null=True, blank=True, help_text='وضعیت')
    pic = models.ImageField('uploaded image', null=True, blank=True, upload_to=scramble_uploaded_filename)

    class Meta:
        ordering = ["taskDate"]

    def __str__(self):
        return str(self.user.username) + " - " + self.project.title + " - " + self.title

    @property
    def owner(self):
        return self.user


class MonthSalary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, help_text='کارمند')
    salaryDate = models.DateField(default=timezone.now, help_text='تاریخ واریز حقوق')
    money = models.BigIntegerField(null=True, blank=True, help_text='حقوق')
    description = models.CharField(max_length=120, null=True, blank=True, help_text='توضیحات')
    workHour = models.CharField(max_length=120, null=True, blank=True, help_text='ساعات کاری')
    pic = models.ImageField('uploaded image', null=True, blank=True, upload_to=scramble_uploaded_filename, help_text='تصویر')


    class Meta:
        ordering = ["salaryDate"]

    def __str__(self):
        return self.employee.fullName + " - " + str(self.id)

    @property
    def owner(self):
        return self.user


class WorkDay(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, help_text='کارمند')
    description = models.CharField(max_length=120, null=True, blank=True, help_text='توضیحات')
    workDate = models.DateField(default=timezone.now, help_text='تاریخ کاری')
    workHour = models.CharField(max_length=120, null=True, blank=True, help_text='ساعات کاری')

    class Meta:
        ordering = ["workDate"]

    def __str__(self):
        return str(self.user.username) + " - " + self.employee.fullName

    @property
    def owner(self):
        return self.user


class CompanyEquipment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    description = models.CharField(max_length=120, null=True, blank=True, help_text='توضیحات')
    pic = models.ImageField('uploaded image', null=True, blank=True, upload_to=scramble_uploaded_filename)
    buyDate = models.DateField(default=timezone.now, help_text='تاریخ خرید')
    price = models.BigIntegerField(null=True, blank=True, help_text='هزینه')

    class Meta:
        ordering = ["buyDate"]

    def __str__(self):
        return str(self.user.username) + " - " + self.title

    @property
    def owner(self):
        return self.user


class Debt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, help_text='کارمند')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    description = models.CharField(max_length=120, null=True, blank=True, help_text='توضیحات')
    status = models.CharField(max_length=120, null=True, blank=True, help_text='وضعیت پرداخت')
    debtDate = models.DateField(default=timezone.now, help_text='تاریخ بدهی')
    paymentDebtDate = models.DateField(default=timezone.now, help_text='تاریخ پرداخت')
    price = models.BigIntegerField(null=True, blank=True, help_text='هزینه')

    class Meta:
        ordering = ["debtDate"]

    def __str__(self):
        return str(self.user.username) + " - " + self.title

    @property
    def owner(self):
        return self.user

