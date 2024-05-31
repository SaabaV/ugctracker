from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies')
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    name = models.CharField(max_length=100)
    info = models.TextField()
    website = models.URLField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    contact_person = models.CharField(max_length=100, default='manager')

    NICHE_CHOICES = [
        ('EC', 'Electronics & Computers'),
        ('FU', 'Furniture'),
        ('HP', 'Home Products'),
        ('CS', 'Cosmetics, skin & hair care'),
        ('TC', 'Toys and products for children'),
        ('CL', 'Clothes and shoes'),
        ('SH', 'Sports and hobbies'),
        ('FD', 'Food and drink'),
        ('OT', 'Others')
    ]

    CONTACTED_VIA_CHOICES = [
        ('NC', 'Email'),
        ('DI', 'Instagram'),
        ('CC', 'TikTok'),
        ('RE', 'Other')
    ]

    COLLABORATION_STATUS_CHOICES = [
        ('NC', 'Not contacted'),
        ('DI', 'In discussion'),
        ('CC', 'The deal is closed'),
        ('RE', 'Rejection')
    ]

    contacted_via = models.CharField(max_length=2, choices=CONTACTED_VIA_CHOICES, default='OT')
    collaboration_status = models.CharField(max_length=2, choices=COLLABORATION_STATUS_CHOICES)
    deal_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    content_count = models.IntegerField(null=True, blank=True)
    niche = models.CharField(max_length=2, choices=NICHE_CHOICES, default='OT')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    companies = models.ManyToManyField(Company, related_name='users')

    def __str__(self):
        return self.user.username


class CompanyRanker:
    def __init__(self, companies):
        self.companies = companies

    def sort_by_name(self):
        self.companies = self.companies.order_by('name')

    def sort_by_status(self):
        self.companies = self.companies.order_by('collaboration_status')

    def search_by_name(self, search_query):
        return self.companies.filter(name__icontains=search_query)

    def search_by_status(self, search_query):
        return self.companies.filter(collaboration_status__icontains=search_query)

    def search_by_niche(self, search_query):
        return self.companies.filter(niche__icontains=search_query)

    def clear_filters(self):
        return self.companies.all()


companies = Company.objects.all()
ranker = CompanyRanker(companies)

ranker.sort_by_name()
sorted_companies_by_name = ranker.companies  # Отсортированный QuerySet

ranker.sort_by_status()
sorted_companies_by_status = ranker.companies  # Отсортированный QuerySet

filtered_companies_by_name = ranker.search_by_name('A')  # Отфильтрованный QuerySet
filtered_companies_by_status = ranker.search_by_status('Not contacted')  # Отфильтрованный QuerySet
filtered_companies_by_niche = ranker.search_by_niche('Tech')  # Отфильтрованный QuerySet

all_companies = ranker.clear_filters()  # Все компании без фильтров

