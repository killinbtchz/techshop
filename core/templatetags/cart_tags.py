from django import template

register = template.Library()

@register.simple_tag()
def hi(value):
    return 'Hello!!'

