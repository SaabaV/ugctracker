from django import forms
from .models import Profile
from .models import ProfileCompany


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'goal', 'date_of_birth']
        widgets = {
            'goal': forms.Select(choices=Profile.DEAL_GOALS),  # Используем Select виджет для выбора
        }


class ProfileCompanyForm(forms.ModelForm):
    class Meta:
        model = ProfileCompany
        fields = ['collaboration_status', 'deal_amount', 'content_count', 'custom_info']
        widgets = {
            'collaboration_status': forms.Select(choices=ProfileCompany.COLLABORATION_STATUS_CHOICES),
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'goal', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

