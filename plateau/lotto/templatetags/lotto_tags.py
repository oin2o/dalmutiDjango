from django import template

register = template.Library()


@register.filter(name='times')
def times(num):
    return range(num)


@register.filter(name='clicked')
def clicked(balls, ball):
    if ball in balls:
        return True
    return False
