from django import template

register = template.Library()

@register.filter(name='get_id')
def get_id(dict, key):
    return dict[key]['id']

@register.filter(name='get_title')
def get_title(dict, key):
    return dict[key]['title_long']

@register.filter(name='get_rating')
def get_rating(dict, key):
    return dict[key]['rating']
