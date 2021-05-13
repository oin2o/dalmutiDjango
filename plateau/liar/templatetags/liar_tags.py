from django import template

register = template.Library()


@register.filter(name='detectGuest')
def detectGuest(guests, counter):
    return guests[counter]
