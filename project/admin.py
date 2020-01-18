from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin

from . import models


@admin.register(models.Project)
class ProjectAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    formfield_overrides = {
    }


@admin.register(models.Employee)
class EmployeeAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    formfield_overrides = {
    }


@admin.register(models.Income)
class IncomeAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    formfield_overrides = {
    }


@admin.register(models.CompanyEquipment)
class CompanyEquipmentAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    formfield_overrides = {
    }


@admin.register(models.Debt)
class DebtAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    formfield_overrides = {
    }


@admin.register(models.MonthSalary)
class MonthSalaryAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    formfield_overrides = {
    }


@admin.register(models.WorkDay)
class WorkDayAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    formfield_overrides = {
    }


@admin.register(models.Task)
class TaskAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    formfield_overrides = {
    }


@admin.register(models.Account)
class AccountAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("id", "title", "type", "description",)
    list_filter = ("type",)


@admin.register(models.SubAccount)
class SubAccountAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):

    list_display = ("id", "title", "account", "description",)
    list_filter = ("account",)


@admin.register(models.Transaction)
class TransactionAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    formfield_overrides = {
    }


# admin.site.register(models.Project)
# admin.site.register(models.Employee)
# admin.site.register(models.Income)
# admin.site.register(models.CompanyEquipment)
# admin.site.register(models.Debt)
# admin.site.register(models.MonthSalary)
# admin.site.register(models.WorkDay)
# admin.site.register(models.Task)
