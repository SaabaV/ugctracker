from django.shortcuts import render
from company_service.models import Company
from .forms import CompanySearchForm


def home_page_view(request):
    form = CompanySearchForm(request.GET or None)
    companies = Company.objects.all()

    if form.is_valid():
        name = form.cleaned_data.get('name')
        niche = form.cleaned_data.get('niche')
        if name:
            companies = companies.filter(name__icontains=name)
        if niche:
            companies = companies.filter(niche=niche)

    return render(request, 'home.html', {'form': form, 'companies': companies})

