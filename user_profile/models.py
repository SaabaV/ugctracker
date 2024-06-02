from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from company_service.models import Company


class Profile(models.Model):
    DEAL_GOALS = [
        ('3', '3 successfully closed deals'),
        ('5', '5 successfully closed deals'),
        ('7', '7 successfully closed deals'),
        ('10', '10 successfully closed deals'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    goal = models.CharField(max_length=2, choices=DEAL_GOALS, default='5')
    date_of_birth = models.DateField(blank=True, null=True)
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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    else:
        profile, created = Profile.objects.get_or_create(user=instance)
        if not created:
            instance.profile.save()

