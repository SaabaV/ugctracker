# home_page/forms.py
from django import forms
from company_service.models import Company


class CompanySearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False, label='Company Name')
    niche = forms.ChoiceField(
        choices=[('', 'All')] + Company.NICHE_CHOICES,
        required=False,
        label='Niche'
    )
