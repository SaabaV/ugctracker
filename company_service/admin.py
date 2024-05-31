from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'collaboration_status', 'user')
    search_fields = ('name', 'user__username')
    list_filter = ('collaboration_status',)
    ordering = ('name',)
