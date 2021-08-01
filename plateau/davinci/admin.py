from django.contrib import admin
from .models import User, Game, Gamer, Cards, Card, Honor


admin.site.register(User)
admin.site.register(Game)
admin.site.register(Gamer)
admin.site.register(Cards)
admin.site.register(Card)
admin.site.register(Honor)
