from django import template
from django.forms import BoundField

register = template.Library()

@register.simple_tag
def speedup_input(bound_field: BoundField):
    return bound_field.as_widget(attrs={'class': 'form-control'})


@register.simple_tag
def speedup_output(minutes: int):
    hours = minutes // 60
    remainder_minutes = minutes % 60
    days = hours // 24
    remainder_hours = hours % 24
    return f"{minutes:,}m ({f'{days}D ' if days else ''}{remainder_hours}:{remainder_minutes})"
