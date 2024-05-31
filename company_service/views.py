from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .forms import CompanyForm
from .models import Company
from .models import CompanyRanker
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from user_profile.models import ProfileCompany

@csrf_exempt
@login_required
def add_to_my_company(request):
    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        print('Received company_id:', company_id)  # Добавим логирование
        if company_id:
            try:
                company = Company.objects.get(id=company_id)
                profile = request.user.profile
                profile_company, created = ProfileCompany.objects.get_or_create(profile=profile, company=company)
                if created:
                    profile_company.collaboration_status = 'NC'  # 'Not contacted' in abbreviation form
                    profile_company.save()
                return JsonResponse({'message': 'Company added to your profile successfully!'})
            except Company.DoesNotExist:
                return JsonResponse({'error': 'Company does not exist'}, status=400)
        else:
            print('Company ID not provided')
            return JsonResponse({'error': 'Company ID not provided'}, status=400)
    else:
        print('Invalid request method:', request.method)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def delete_from_profile(request):
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        profile_company = get_object_or_404(ProfileCompany, profile=request.user.profile, company_id=company_id)
        profile_company.delete()
        return JsonResponse({"message": "Company removed from profile successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=400)


def add_company_view(request):
    company_exists = False
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            # Проверяем, существует ли компания с таким именем у текущего пользователя
            if Company.objects.filter(name=name, user=request.user).exists():
                company_exists = True
                messages.error(request, "A company by that name already exists.")
            else:
                company = form.save(commit=False)
                company.user = request.user
                company.save()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'name': company.name, 'collaboration_status': company.get_collaboration_status_display()})
                return redirect('user_profile')
        else:
            messages.error(request, "Error in the form. Please check the entered data.")
    else:
        form = CompanyForm()
    return render(request, 'add_company.html', {'form': form, 'company_exists': company_exists})


def edit_company(request, company_id):
    company = get_object_or_404(ProfileCompany, id=company_id)
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company updated successfully.')
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@csrf_exempt
def delete_company(request):
    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        company = get_object_or_404(Company, pk=company_id)
        company.delete()
        return JsonResponse({'message': 'Company deleted successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def search_view(request):
    search_query = request.GET.get('q', '')
    user = request.user

    companies = Company.objects.filter(user=user)
    ranker = CompanyRanker(companies)

    search_results = {
        'by_name': ranker.search_by_name(search_query),
        'by_status': ranker.search_by_status(search_query)
    }

    results_count = {
        'by_name': len(search_results['by_name']),
        'by_status': len(search_results['by_status'])
    }
    # Преобразуем статусы в slug перед передачей в шаблон
    for result_type in search_results:
        for company in search_results[result_type]:
            company.status_slug = slugify(company.get_collaboration_status_display())

    return render(request, 'search_results.html', {
        'search_query': search_query,
        'search_results': search_results,
        'results_count': results_count
    })

