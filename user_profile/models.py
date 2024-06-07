from django.db import models
from django.contrib.auth.models import User
from company_service.models import Company


class Profile(models.Model):
    DEAL_GOALS = [
        ('3', '3 successfully closed deals'),
        ('5', '5 successfully closed deals'),
        ('7', '7 successfully closed deals'),
        ('10', '10 successfully closed deals'),
        ('15', '15 successfully closed deals'),
        ('25', '25 successfully closed deals'),
        ('50', '50 successfully closed deals'),
        ('75', '75 successfully closed deals'),
        ('100', '100 successfully closed deals'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    goal = models.CharField(max_length=3, choices=DEAL_GOALS, default='5')
    companies = models.ManyToManyField(Company, through='ProfileCompany', related_name='profiles')

    def __str__(self):
        return f'{self.user.username} Profile'


class ProfileCompany(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    deal_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    content_count = models.IntegerField(null=True, blank=True)
    custom_info = models.TextField(null=True, blank=True)

    COLLABORATION_STATUS_CHOICES = [
        ('NC', 'Not contacted'),
        ('DI', 'In discussion'),
        ('CC', 'The deal is closed'),
        ('RE', 'Rejection')
    ]
    collaboration_status = models.CharField(max_length=100, choices=COLLABORATION_STATUS_CHOICES, default='NC')

    def __str__(self):
        return f"{self.profile.user.username} - {self.company.name}"




