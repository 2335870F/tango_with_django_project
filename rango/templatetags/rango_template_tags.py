from django import template
from rango.models import Category

register = template.Library()
@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(),
            'act_cat': cat}
    #This method returns a list of categories but is mashed up witht he template rango/cats.html
