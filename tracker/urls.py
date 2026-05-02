from django.urls import path
from django.contrib.auth import views as auth_views # Import koro
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('check-in/', views.check_in, name='check_in'),
    path('check-out/', views.check_out, name='check_out'),
    path('toggle-break/', views.toggle_break, name='toggle_break'),
    path('manual-entry/', views.manual_entry, name='manual_entry'),
    path('add-site/', views.add_site, name='add_site'),
    path('export-attendance/', views.export_attendance, name='export_attendance'),
    path('signup/', views.signup, name='signup'),
]