from django import template

from core.models import MainPageInfoBlock


register = template.Library()


@register.inclusion_tag('core/components/infoblock_on_main.html')
def infoblock_query():
    blocks = MainPageInfoBlock.visible.all()
    return {'blocks': blocks}
