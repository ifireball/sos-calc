from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def same_view_url(context, *args, **kwargs):
    view, vargs, vkwargs = context.request.resolver_match
    vkwargs = vkwargs.copy()
    vkwargs.update(kwargs)
    return reverse(view, args=(args or vargs), kwargs=vkwargs)
