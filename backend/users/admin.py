from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import MyUser, Subscription

admin.site.register(MyUser, UserAdmin)
admin.site.register(Subscription)
