from django import template

register = template.Library()


@register.filter(name='detectGuest')
def detectGuest(guests, counter):
    return guests[counter]


@register.filter(name='caculCardOrder')
def caculCardOrder(order):
    return order + 1

@register.filter(name='caculCardOrderDesc')
def caculCardOrderDesc(order):
    return order - 1

@register.filter(name='times')
def times(num):
    return range(num)
