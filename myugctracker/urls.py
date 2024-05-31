"""
URL configuration for myugctracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users.views import registration_view, login_view
from user_profile.views import upload_avatar
from company_service.views import edit_company, search_view
from company_service import views
from user_profile.views import user_profile
import home_page.urls
from user_profile import views as user_profile_views

urlpatterns = [
    path('home/', include(home_page.urls)),
    path('add_to_my_company/', views.add_to_my_company, name='add_to_my_company'),
    path('user_profile/', include('user_profile.urls')),
    path('edit_profile/', user_profile_views.edit_profile, name='edit_profile'),
    path('search/', views.search_view, name='search_results'),
    path('search/', search_view, name='search'),
    path('delete_from_profile/', views.delete_from_profile, name='delete_from_profile'),
    path('edit_company/<int:company_id>/', edit_company, name='edit_company'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('upload_avatar/', upload_avatar, name='upload_avatar'),
    path('add_company/', views.add_company_view, name='add_company'),
    path('profile/add_company/', views.add_company_view, name='add_company_view'),
    path('', registration_view, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('profile/', user_profile, name='user_profile'),
    path('login/', login_view, name='login'),
    path('register/', registration_view, name='register'),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
