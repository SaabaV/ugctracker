from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from .models import ProfileCompany, Profile
from .forms import ProfileForm
from company_service.models import Company
from company_service.models import CompanyRanker
from .forms import ProfileCompanyForm


@login_required
def edit_profile_company(request, profile_company_id):
    profile_company = get_object_or_404(ProfileCompany, id=profile_company_id, profile=request.user.profile)
    if request.method == 'POST':
        form = ProfileCompanyForm(request.POST, instance=profile_company)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False, 'errors': 'Invalid request method'}, status=400)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'message': 'Profile updated successfully',
                'date_of_birth': request.user.profile.date_of_birth
            })
        else:
            errors = form.errors.as_json()
            print('Form errors:', errors)
            return JsonResponse({'error': 'Form is not valid', 'details': errors}, status=400)
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


# Обработчик для сохранения цели
def save_goal(request):
    if request.method == 'POST':
        goal = request.POST.get('goal')
        if goal:
            profile = request.user.profile
            profile.goal = goal
            profile.save()
            return JsonResponse({'message': 'Goal updated successfully', 'goal': profile.get_goal_display()})
        return JsonResponse({'error': 'Goal not provided'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def user_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    profile_companies = user.profile.profilecompany_set.all()

    # Подсчет количества компаний по каждому статусу
    status_counts = {
        'CC': profile_companies.filter(collaboration_status='CC').count(),
        'DI': profile_companies.filter(collaboration_status='DI').count(),
        'NC': profile_companies.filter(collaboration_status='NC').count(),
        'RE': profile_companies.filter(collaboration_status='RE').count()
    }

    context = {
        'user': user,
        'profile': profile,
        'profile_companies': profile_companies,
        'status_counts': status_counts,
        'collaboration_status_choices': ProfileCompany.COLLABORATION_STATUS_CHOICES,
    }
    return render(request, 'user_profile.html', context)


def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'user_profile.html', {'form': form})


@login_required
def search_view(request):
    search_query = request.GET.get('q', '')
    user = request.user

    companies = Company.objects.filter(user=user)
    ranker = CompanyRanker(companies)

    search_results = {
        'by_name': ranker.search_by_name(search_query),
        'by_status': ranker.search_by_status(search_query),
        'by_niche': ranker.search_by_niche(search_query)
    }

    results_count = {
        'by_name': len(search_results['by_name']),
        'by_status': len(search_results['by_status']),
        'by_niche': len(search_results['by_niche'])
    }

    for result_type in search_results:
        for company in search_results[result_type]:
            company.status_slug = slugify(company.get_collaboration_status_display())

    return render(request, 'search_results.html', {
        'search_query': search_query,
        'search_results': search_results,
        'results_count': results_count
    })


def upload_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        # Получить загруженное изображение
        uploaded_avatar = request.FILES['avatar']

        # Сохранить изображение на сервере
        file_path = default_storage.save('avatars/' + uploaded_avatar.name, uploaded_avatar)

        # Обновить профиль пользователя
        request.user.profile.avatar = file_path
        request.user.profile.save()

        return redirect('user_profile')
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

