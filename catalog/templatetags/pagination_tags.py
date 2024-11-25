from django import template
from urllib.parse import urlencode

register = template.Library()


@register.simple_tag
def url_with_query_params(request, page_number=None):
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    if page_number is not None:
        query_params['page'] = page_number
    return f"?{urlencode(query_params)}"
