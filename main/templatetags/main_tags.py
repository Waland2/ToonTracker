from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    
    if 'cartoons_only' in query:
        del query['cartoons_only']

    return query.urlencode()