from django.shortcuts import render
import math
from company_service.models import Company
from .forms import CompanySearchForm, DealCalculatorForm


def home_page_view(request):
    form = CompanySearchForm(request.GET or None)
    calculator_form = DealCalculatorForm(request.POST or None)
    companies = Company.objects.all()
    result = None

    if form.is_valid():
        name = form.cleaned_data.get('name')
        niche = form.cleaned_data.get('niche')
        if name:
            companies = companies.filter(name__icontains=name)
        if niche:
            companies = companies.filter(niche=niche)

    if calculator_form.is_valid():
        price_per_unit = calculator_form.cleaned_data['price_per_unit']
        target_amount = calculator_form.cleaned_data['target_amount']

        required_deals = target_amount / price_per_unit
        result = math.ceil(required_deals)

    return render(request, 'home.html', {'form': form, 'companies': companies, 'calculator_form': calculator_form, 'result': result})
