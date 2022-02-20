from django.contrib import admin
from .models import User, Location, Egg, Abandon, EggLocation


admin.site.register(User)
admin.site.register(Location)
admin.site.register(Egg)
admin.site.register(Abandon)
admin.site.register(EggLocation)
