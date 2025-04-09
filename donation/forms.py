from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import User, Donor, OrganRequest, Testimonial, ContactMessage

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DonorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['full_name', 'age', 'blood_type', 'organ_to_donate', 'contact_number', 'address']

class OrganRequestForm(forms.ModelForm):
    class Meta:
        model = OrganRequest
        fields = ['donor', 'requested_organ']

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['message']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class DonorUpdateForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['full_name', 'age', 'blood_type', 'organ_to_donate', 'contact_number', 'address']

class PasswordChangingForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']