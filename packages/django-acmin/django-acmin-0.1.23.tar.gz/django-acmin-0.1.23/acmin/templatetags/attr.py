import datetime

from django import template

from acmin.utils import attr as u

register = template.Library()


@register.filter
def attr(value, attr_name):
    result = u(value, attr_name, default="")
    if isinstance(result, bool):
        result = "是" if result else '否'
    elif isinstance(result, datetime.datetime):
        result = result.strftime("%Y-%m-%d %H:%M:%S")
    return result
