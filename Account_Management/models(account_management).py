# Account_Management: Contains tables related to account (company level) information and settings.
# This would include details of the organizations or individuals or user invitation using the system.

from django.db import models
from user_management.models import User


# Description: Stores account-level (aka company-level) details, such as the account name, date created, account owner (link to Auth_User), etc.
class Account(models.Model):
    ACCOUNT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('fraud', 'Fraud'),
    ]

    COMPANY_SIZE_RANGE_CHOICES = [
        ('1-50', '1-50'),
        ('51-200', '51-200'),
        ('201-500', '201-500'),
        ('501-1000', '501-1000'),
        ('1001+', '1001+'),
    ]

    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_email = models.EmailField(max_length=255, null=True, blank=True)
    account_status = models.CharField(
        max_length=255, choices=ACCOUNT_STATUS_CHOICES)
    company_summary = models.TextField(null=True, blank=True)
    company_industry = models.CharField(max_length=255, null=True, blank=True)
    company_size_range = models.CharField(
        max_length=255, null=True, blank=True, choices=COMPANY_SIZE_RANGE_CHOICES)
    company_website = models.URLField(max_length=255, null=True, blank=True)
    company_location = models.CharField(max_length=255, null=True, blank=True)
    company_domain = models.CharField(max_length=255, unique=True)
    logo_url = models.URLField(max_length=255, null=True, blank=True)
    company_linkedin = models.URLField(max_length=255, null=True, blank=True)
    company_facebook = models.URLField(max_length=255, null=True, blank=True)
    company_twitter = models.URLField(max_length=255, null=True, blank=True)
    company_video_url = models.URLField(max_length=255, null=True, blank=True)
    viewed_employer_welcome = models.TextField(null=True, blank=True)
    viewed_employer_tutorial = models.TextField(null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=255, unique=True)
    stripe_subscription_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True)
    trial_starts_at = models.DateTimeField()
    trial_end_at = models.DateTimeField()
    is_free_trial = models.BooleanField(default=True)
    payg_credit = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['company_name']),
            models.Index(fields=['account_status']),
            models.Index(fields=['company_industry']),
            models.Index(fields=['company_domain']),
        ]


# Description: Stores different roles available in the system, like 'admin', 'recruiter', 'interviewer', etc.
class Role(models.Model):
    ROLE_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('hiring_manager', 'Hiring_Manager'),
        ('recruiter', 'Recruiter'),
        ('coordinator', 'Coordinator'),
        ('sourcer', 'Sourcer'),
        ('external_reviewer', 'External_Reviewer'),
        ('sub_reviewer', 'Sub_Reviewer'),
    ]

    role_name = models.CharField(max_length=255, unique=True)
    role_type = models.CharField(max_length=255, choices=ROLE_TYPE_CHOICES)
    role_description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['role_type']),
        ]


# Description: Manages invitations to join a team. Fields could include invitation ID, team ID, invitee email, status of the invitation, etc.
class TeamInvitation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='team_invitations')
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    invited_email = models.EmailField()
    is_accepted = models.BooleanField(default=False)
    invited_by_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_invitations')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['account']),
            models.Index(fields=['invited_email']),
            models.Index(fields=['is_accepted']),
            models.Index(fields=['role']),
        ]


# Description: Stores the teams within an account. Could include team ID, account ID, and the team name.
class HiringTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey('job_management.Job', on_delete=models.CASCADE)
    team_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['job']),
        ]
