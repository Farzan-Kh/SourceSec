from django import template

register = template.Library()

@register.filter
def skip_parents(value, num_parents=3):
    parts = value.split('/')
    if len(parts) > num_parents:
        return './' + '/'.join(parts[num_parents:])
    return value