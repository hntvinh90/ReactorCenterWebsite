from django import template

from libs import custom_filters

register = template.Library()

register.filter('split', custom_filters.split)
