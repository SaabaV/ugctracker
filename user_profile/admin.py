# admin.py

from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'goal', 'date_of_birth']
    search_fields = ('user_username', 'bio')
    list_filter = ('date_of_birth',)
    fieldsets = (
        (None, {
            'fields': ('user', 'goal', 'date_of_birth', 'avatar')
        }),
    )


