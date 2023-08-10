from django import template

register = template.Library()


@register.filter(name="replace")
def replace(value, arg):
    """Replace all values of arg to space"""
    return value.replace(arg, " ")
