from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.


class UserprofileInline(admin.StackedInline):
    model = UserProfile


class Useradmin(UserAdmin):
    inlines = (UserprofileInline, )


admin.site.unregister(User)
admin.site.register(User, Useradmin)
admin.site.register(UserProfile)
