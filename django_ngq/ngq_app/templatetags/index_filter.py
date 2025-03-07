from django import template

register = template.Library()

# Register index filter for easier use of indices in rendering
@register.filter
def index(list, i):
    try:
        return list[i]
    except IndexError:
        return None