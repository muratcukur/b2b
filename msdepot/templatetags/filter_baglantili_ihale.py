from django import template

register = template.Library()

@register.filter
def in_category(baglantili, ihale):
    return baglantili.filter(baglantiliihaleid=ihale)