from django.contrib import admin
from .models import User, Location, Egg, Abandon, EggLocation


class UserAdmin(admin.ModelAdmin):
    ordering = ['-useYn', 'username']


class LocationAdmin(admin.ModelAdmin):
    ordering = ['loctnum']


class EggAdmin(admin.ModelAdmin):
    ordering = ['-useYn', 'eggname']


class EggLocationAdmin(admin.ModelAdmin):
    ordering = ['egg__eggname', 'location__loctnum']


admin.site.register(User, UserAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Egg, EggAdmin)
admin.site.register(EggLocation, EggLocationAdmin)
admin.site.register(Abandon)
