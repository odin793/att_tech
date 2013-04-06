from django import template
from django.conf import settings
from att_tech_app.models import New 

register = template.Library()

@register.inclusion_tag('news_block_template.html')
def news_block():
    last_news = New.objects.all().order_by('-date_added')[:7]
    return {'last_news': last_news}