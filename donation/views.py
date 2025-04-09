from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import *
from .models import *

class ChangePasswordView(PasswordChangeView):
    template_name = 'donation/change_password.html'
    success_url = reverse_lazy('profile')

def home(request):
    donors = Donor.objects.filter(is_approved=True)
    requests = OrganRequest.objects.all()
    testimonials = Testimonial.objects.all()[:3]

    context = {
        'total_donors': donors.count(),
        'total_requests': requests.count(),
        'approved_requests': requests.filter(status='Approved').count(),
        'recent_donors': donors.order_by('-id')[:2],
        'recent_requests': requests.order_by('-request_date')[:2],
        'testimonials': testimonials,
    }
    return render(request, 'donation/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'donation/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'donation/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

@login_required
def register_donor(request):
    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            donor = form.save(commit=False)
            donor.user = request.user
            donor.save()
            request.user.is_donor = True
            request.user.save()
            messages.success(request, 'Donor registration submitted for approval!')
            return redirect('profile')
    else:
        form = DonorRegistrationForm()
    return render(request, 'donation/register_donor.html', {'form': form})

@login_required
def request_organ(request):
    donors = Donor.objects.filter(is_approved=True)
    if request.method == 'POST':
        form = OrganRequestForm(request.POST)
        if form.is_valid():
            organ_request = form.save(commit=False)
            organ_request.recipient = request.user
            organ_request.save()
            messages.success(request, 'Organ request submitted!')
            return redirect('my_requests')
    else:
        form = OrganRequestForm()
    return render(request, 'donation/request_organ.html', {'form': form, 'donors': donors})

@login_required
def profile(request):
    donor = None
    if request.user.is_donor:
        donor = Donor.objects.get(user=request.user)
    requests = OrganRequest.objects.filter(recipient=request.user)
    return render(request, 'donation/profile.html', {'donor': donor, 'requests': requests})

@login_required
def update_donor(request):
    donor = get_object_or_404(Donor, user=request.user)
    if request.method == 'POST':
        form = DonorUpdateForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donor information updated!')
            return redirect('profile')
    else:
        form = DonorUpdateForm(instance=donor)
    return render(request, 'donation/update_donor.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangingForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
    else:
        form = PasswordChangingForm(request.user)
    return render(request, 'donation/change_password.html', {'form': form})

def testimonials(request):
    testimonials = Testimonial.objects.all()
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            messages.success(request, 'Testimonial submitted!')
            return redirect('testimonials')
    else:
        form = TestimonialForm()
    return render(request, 'donation/testimonials.html', {'form': form, 'testimonials': testimonials})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'donation/contact.html', {'form': form})

def about(request):
    return render(request, 'donation/about.html')

def awareness(request):
    return render(request, 'donation/awareness.html')

def faqs(request):
    return render(request, 'donation/faqs.html')

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    users = User.objects.all()
    organ_requests = OrganRequest.objects.all()
    contact_messages = ContactMessage.objects.all()
    testimonials = Testimonial.objects.all()

    if request.method == 'POST' and 'approve_request' in request.POST:
        request_id = request.POST.get('request_id')
        organ_request = OrganRequest.objects.get(id=request_id)
        organ_request.status = 'Approved'
        organ_request.save()
        messages.success(request, 'Request approved!')
        return redirect('admin_dashboard')

    if request.method == 'POST' and 'reject_request' in request.POST:
        request_id = request.POST.get('request_id')
        organ_request = OrganRequest.objects.get(id=request_id)
        organ_request.status = 'Rejected'
        organ_request.save()
        messages.success(request, 'Request rejected!')
        return redirect('admin_dashboard')

    context = {
        'users': users,
        'organ_requests': organ_requests,
        'contact_messages': contact_messages,
        'testimonials': testimonials,
    }
    return render(request, 'donation/admin_dashboard.html', context)
