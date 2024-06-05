# home_page/forms.py
from django import forms
from company_service.models import Company


class DealCalculatorForm(forms.Form):
    price_per_unit = forms.IntegerField(label='Price per content unit', min_value=0)
    target_amount = forms.IntegerField(label='Desired earnings amount', min_value=0)
    currency = forms.ChoiceField(label='Currency', choices=[('USD', 'USD'), ('EUR', 'EUR')], initial='EUR')


class CompanySearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False, label='Company Name')
    niche = forms.ChoiceField(
        choices=[('', 'All')] + Company.NICHE_CHOICES,
        required=False,
        label='Niche'
    )
