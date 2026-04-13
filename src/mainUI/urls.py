from django.contrib import admin
from django.urls import include, path

# import mainUI.views as views
# urls.py
from django.urls import path
from . import views

# app_name = 'authentication'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('update-file-store/', views.update_file_store_view, name='update_file_store'),
    path('update-main-file/', views.update_main_file_view, name='update_main_file'),
    path('profile/', views.get_user_profile_view, name='profile'),
    path("editor", views.editor),
    path("editor1", views.main),
    path("testing", views.testing),
    path("",views.homepage),

]
