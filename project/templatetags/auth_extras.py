from django import template
from django.contrib.auth.models import Group
from datetime import date

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    # print(user.groups)
    return user.groups.filter(name=group_name).exists()


# @register.filter(name='has_abedi')
# def has_abedi(user):
#     # return user.username == "d_abedi" and user.is_superuser
#     return user.is_superuser
#
#
# @register.filter(name='is_past_due')
# def is_past_due(self, m_date):
#     return date.today() <= m_date


@register.filter(name='is_true')
def is_true(self, m_date):
    if m_date == 'true':
        return 'checked'
    else:
        return 'unchecked'


@register.filter(name='is_selected')
def is_selected(self, m_date):
    if str(self) in m_date:
        return 'selected'
    else:
        return ''
