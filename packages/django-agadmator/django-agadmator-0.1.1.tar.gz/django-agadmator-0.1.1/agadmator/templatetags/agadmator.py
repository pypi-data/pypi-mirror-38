from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def set_qsarg(context, *args):

    query_dict = context['request'].GET.copy()
    for key, val in zip(args[::2], args[1::2]):
        query_dict[str(key)] = str(val)
    return '?' + query_dict.urlencode()
