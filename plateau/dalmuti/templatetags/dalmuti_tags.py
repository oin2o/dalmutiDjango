from django import template

register = template.Library()


@register.filter(name='addtion')
def addtion(value, arg):
    return value + arg


@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg


@register.filter(name='checkquit')
def checkquit(gamer, total_gamer):
    if gamer.game.ingameCd == 0:
        if gamer not in total_gamer.exclude(position=0).order_by('position'):
            return True
        elif len(total_gamer) == 1:
            return True

    return False


@register.filter(name='checkshuffle')
def checkshuffle(user, total_gamer):
    gamer = total_gamer.filter(user=user).first()
    gamer_list = total_gamer.filter(position=0)
    ready_gamer_list = total_gamer.exclude(position=0)

    if gamer.game.ingameCd == 0 and len(ready_gamer_list) >= 4 and len(gamer_list) == 0 and gamer.game.turnUser.username == gamer.user.username:
        return True
    elif gamer.game.ingameCd == 4 and gamer.game.round != 13 and gamer.game.turnUser.username == gamer.user.username:
        return True

    return False


@register.filter(name='carddrawavailable')
def carddrawavailable(gamer, cards):
    if gamer.game.drawusername == gamer.user.username:
        return True
    elif len(cards) >= gamer.game.lastCardCnt:
        cards_list = list(cards.filter(card__lte=gamer.game.lastCard-1).values_list('card', flat=True))
        cards_set = sorted(set(cards_list))
        isdrawavailable = False
        for card_set in cards_set:
            if cards_list.count(card_set) + gamer.jokerCnt >= gamer.game.lastCardCnt:
                isdrawavailable = True
                break
        if isdrawavailable and gamer.game.lastCard > cards[0].card and len(cards) >= gamer.game.lastCardCnt:
            return True

    return False


@register.filter(name='islastgamer')
def islastgamer(total_gamer):

    incomplete_gamers = total_gamer.exclude(cardTotCnt=0)

    if len(incomplete_gamers) == 1:
        return True

    return False


@register.filter(name='isingame')
def isingame(gamer):
    if gamer.game.ingameCd == 3:
            return True

    return False
