from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_donor = models.BooleanField(default=False)
    is_recipient = models.BooleanField(default=False)

class Donor(models.Model):
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    
    ORGAN_CHOICES = [
        ('Heart', 'Heart'),
        ('Liver', 'Liver'),
        ('Kidney', 'Kidney'),
        ('Lungs', 'Lungs'),
        ('Pancreas', 'Pancreas'),
        ('Corneas', 'Corneas'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES)
    organ_to_donate = models.CharField(max_length=20, choices=ORGAN_CHOICES)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.full_name

class OrganRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    requested_organ = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    request_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.recipient.username} - {self.requested_organ}"

class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Testimonial by {self.user.username}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.subject