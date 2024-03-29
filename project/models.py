from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
import uuid


def scramble_uploaded_filename(instance, filename):
    extention = filename.split(".")[-1]
    return "{}.{}".format(uuid.uuid4(), extention)


PROJECT_STATUS_CHOICES = (
    ("0", "انجام شده"),
    ("1", "متوقف"),
    ("2", "تعلیق"),
    ("3", "در حال انجام"),
    ("4", "طرح ریزی"),
)


class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, help_text='کاربر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان پروژه')
    projectOwner = models.CharField(max_length=120, null=True, blank=True, help_text='کارفرما')
    pic = models.ImageField('uploaded image', null=True, blank=True, upload_to=scramble_uploaded_filename, help_text='تصویر')
    startDate = models.DateField(default=timezone.now, help_text='شروع پروژه')
    deadline = models.DateField(default=timezone.now, help_text='تاریخ اتمام پروژه')
    money = models.BigIntegerField(null=True, blank=True, help_text='هزینه پروژه')
    status = models.CharField(max_length=120, null=True, blank=True, help_text='وضعیت پروژه', choices=PROJECT_STATUS_CHOICES, default='4')
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


# remove
class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    pic = models.ImageField('uploaded image', null=True, blank=True, upload_to=scramble_uploaded_filename)
    incomeDate = models.DateField(default=timezone.now)
    money = models.BigIntegerField(null=True, blank=True)
    description = models.CharField(max_length=120, null=True, blank=True, help_text='توضیحات')
    isOutcome = models.BooleanField(default=True, help_text='هزینه-درآمد')

    class Meta:
        ordering = ["incomeDate"]

    def __str__(self):
        return str(self.user.username) + " - " + self.project.title + " - " + str(self.incomeDate)

    @property
    def owner(self):
        return self.user


TASK_STATUS_CHOICES = (
    ("0", "تعریف شده"),
    ("1", "در حال انجام"),
    ("2", "انجام شده"),
    ("3", "متوقف"),
    ("4", "تعلیق"),
)


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # employees = models.ManyToManyField(Employee)
    employees = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    taskDate = models.DateField(default=timezone.now)
    dueDate = models.DateField(default=timezone.now)
    description = models.CharField(max_length=120, null=True, blank=True, help_text='توضیحات')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    status = models.CharField(max_length=50, null=True, blank=True, help_text='وضعیت', choices=TASK_STATUS_CHOICES, default='4')
    pic = models.ImageField('uploaded image', null=True, blank=True, upload_to=scramble_uploaded_filename)

    class Meta:
        ordering = ["taskDate"]

    def __str__(self):
        return str(self.user.username) + " - " + self.project.title + " - " + self.title

    @property
    def owner(self):
        return self.user


# remove
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


# remove
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


# remove
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


ACCOUNT_CHOICES = (
    ("0", "سرمایه"),
    ("1", "بدهی"),
    ("2", "دارایی"),
)


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    description = models.CharField(max_length=120, null=True, blank=True, help_text='توضیحات')
    type = models.CharField(max_length=120, null=True, blank=True, help_text='نوع', choices=ACCOUNT_CHOICES, default='2')
    pic = models.ImageField('uploaded image', null=True, blank=True, upload_to=scramble_uploaded_filename, help_text='آیکون')

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title + " - " + self.get_type_display()

    @property
    def owner(self):
        return self.user


class SubAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان زیرشاخه حساب')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, help_text='حساب')
    description = models.CharField(max_length=120, null=True, blank=True, help_text='توضیحات')
    pic = models.ImageField('uploaded image', null=True, blank=True, upload_to=scramble_uploaded_filename, help_text='آیکون')

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return str(self.user.username) + " - " + self.title

    @property
    def owner(self):
        return self.user


TRANSACTION_CHOICES = (
    ("0", "دریافت"),
    ("1", "پرداخت"),
    ("2", "انتقال"),
)


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE, help_text='پروژه')
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.CASCADE, help_text='کارمند')
    source = models.ForeignKey(SubAccount, related_name='sourceAccount', on_delete=models.CASCADE, help_text='حساب مبدا')
    destination = models.ForeignKey(SubAccount, related_name='destinationAccount', on_delete=models.CASCADE, help_text='حساب مقصد')
    pic = models.ImageField('uploaded image', null=True, blank=True, upload_to=scramble_uploaded_filename)
    createdAt = models.DateField(default=timezone.now)
    money = models.BigIntegerField(null=True, blank=True, help_text='مبلغ')
    description = models.CharField(max_length=120, null=True, blank=True, help_text='توضیحات')
    type = models.CharField(max_length=120, null=True, blank=True, help_text='نوع', choices=TRANSACTION_CHOICES, default='1')

    class Meta:
        ordering = ["createdAt"]

    def __str__(self):
        return str(self.user.username) + " - " + self.project.title + " - " + str(self.createdAt)

    @property
    def owner(self):
        return self.user
