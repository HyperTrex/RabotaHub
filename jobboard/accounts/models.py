from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPE = [
        ('employer', 'Employer'),
        ('seeker', 'Job Seeker'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE)

    # for job seekers
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)
    skills = models.TextField(blank=True)

    # for employers
    company_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username