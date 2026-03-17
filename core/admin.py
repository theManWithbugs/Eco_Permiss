from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *

admin.site.register(Ugai)
admin.site.register(User, UserAdmin)