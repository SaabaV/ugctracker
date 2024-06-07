# admin.py

from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'goal']
    search_fields = ('user_username', 'bio')
    fieldsets = (
        (None, {
            'fields': ('user', 'goal', 'avatar')
        }),
    )


