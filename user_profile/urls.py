# user_profile/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('edit_profile_company/<int:profile_company_id>/', views.edit_profile_company, name='edit_profile_company'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('save_goal/', views.save_goal, name='save_goal'),
]
