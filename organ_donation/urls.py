from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from donation import views
from donation.views import ChangePasswordView  # Updated import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register-donor/', views.register_donor, name='register_donor'),
    path('request-organ/', views.request_organ, name='request_organ'),
    path('profile/', views.profile, name='profile'),
    path('update-donor/', views.update_donor, name='update_donor'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),  # Updated line
    path('testimonials/', views.testimonials, name='testimonials'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('awareness/', views.awareness, name='awareness'),
    path('faqs/', views.faqs, name='faqs'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Password reset URLs
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='donation/password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='donation/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='donation/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='donation/password_reset_complete.html'), 
         name='password_reset_complete'),
]
