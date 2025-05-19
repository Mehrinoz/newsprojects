from django.contrib import admin

from accounts.models import UserProfile


class AdminProfile(admin.ModelAdmin):
    list_display = ['user','date_of_birth']


admin.site.register(UserProfile,AdminProfile)
