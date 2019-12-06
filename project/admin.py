from django.contrib import admin

from . import models

admin.site.register(models.Project)
admin.site.register(models.Employee)
admin.site.register(models.Income)
admin.site.register(models.CompanyEquipment)
admin.site.register(models.Debt)
admin.site.register(models.MonthSalary)
admin.site.register(models.WorkDay)
admin.site.register(models.Task)