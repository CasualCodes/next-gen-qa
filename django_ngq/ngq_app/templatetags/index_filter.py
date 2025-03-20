from django import template

## References
# - https://docs.djangoproject.com/en/5.1/howto/custom-template-tags/
# - Microsoft Copilot advice

register = template.Library()

# Register index filter for easier use of indices in rendering
@register.filter
def index(list, i):
    try:
        return list[i]
    except IndexError:
        return None