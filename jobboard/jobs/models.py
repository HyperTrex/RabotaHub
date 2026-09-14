from django.db import models
from django.contrib.auth.models import User



class Job(models.Model):
    CATEGORY_CHOICES = [
        ('IT', 'IT'),
        ('Marketing', 'Marketing'),
        ('Design', 'Design'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    salary = models.IntegerField()
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    employer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    
    # Contact info
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    # Direct links
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    
    # CV/Resume upload
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    
    # Screening questions
    work_eligibility = models.CharField(max_length=10, choices=[('yes', 'Yes'), ('no', 'No')], blank=True)
    start_date = models.DateField(blank=True, null=True)
    
    # Cover letter
    cover_letter = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    # Optional job reference
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sender.username} -> {self.recipient.username}: {self.subject}"