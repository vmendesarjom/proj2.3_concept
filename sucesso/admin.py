from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth import admin as auth

from .models import UUIDUser, Conceito, Palavra, Partida

# UserAdmin
# - - - - - - - - - - - - - - - - - - -
class UserAdmin(auth.UserAdmin):

    fieldsets = (
        ('Personal info', {'fields': ('username','first_name', 'last_name', 'password', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(Conceito)
admin.site.register(Palavra)
admin.site.register(Partida)
admin.site.register(UUIDUser, UserAdmin)