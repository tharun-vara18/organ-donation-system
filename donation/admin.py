from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Donor, OrganRequest, Testimonial, ContactMessage

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_donor', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_donor')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, CustomUserAdmin)

class DonorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'blood_type', 'organ_to_donate', 'is_approved')
    list_filter = ('blood_type', 'organ_to_donate', 'is_approved')
    search_fields = ('full_name', 'user__username')

admin.site.register(Donor, DonorAdmin)

class OrganRequestAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'donor', 'requested_organ', 'status', 'request_date')
    list_filter = ('status', 'requested_organ')
    search_fields = ('recipient__username', 'donor__full_name')

admin.site.register(OrganRequest, OrganRequestAdmin)

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_posted')
    search_fields = ('user__username', 'message')

admin.site.register(Testimonial, TestimonialAdmin)

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'date_sent')
    search_fields = ('name', 'email', 'subject')

admin.site.register(ContactMessage, ContactMessageAdmin)